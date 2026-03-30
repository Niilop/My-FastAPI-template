from fastapi import APIRouter, HTTPException, Request, Depends
from langchain_core.prompts import PromptTemplate
from sqlalchemy.orm import Session

from api.endpoints.auth import get_current_user
from core.database import get_db
from core.rate_limit import limiter
from models.database import User
from models.schemas import (
    DocumentIngestRequest,
    DocumentIngestResponse,
    RAGQueryRequest,
    RAGQueryResponse,
)
from services.llm_service import llm
from services.rag_service import ingest_document, retrieve_chunks

router = APIRouter(prefix="/rag", tags=["RAG"])

_rag_prompt = PromptTemplate.from_template(
    "Answer the question using only the context below. "
    "If the context does not contain enough information, say so.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
    "Answer:"
)


@router.post("/ingest", response_model=DocumentIngestResponse)
@limiter.limit("20/minute")
def ingest(
    request: Request,
    body: DocumentIngestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Chunk, embed, and store a document for later retrieval."""
    try:
        n = ingest_document(db, current_user.id, body.source, body.text)
        return DocumentIngestResponse(source=body.source, chunks_created=n)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=RAGQueryResponse)
@limiter.limit("10/minute")
def query(
    request: Request,
    body: RAGQueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve relevant chunks and answer the question with the configured LLM."""
    chunks = retrieve_chunks(db, current_user.id, body.question, k=body.top_k)
    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="No documents found. Ingest some documents first via POST /rag/ingest.",
        )

    context = "\n\n---\n\n".join(c.content for c in chunks)
    chain = _rag_prompt | llm
    response = chain.invoke({"context": context, "question": body.question})

    return RAGQueryResponse(
        answer=response.content,
        sources=list(dict.fromkeys(c.source for c in chunks)),  # dedup, preserve order
        chunks=[c.content for c in chunks],
    )
