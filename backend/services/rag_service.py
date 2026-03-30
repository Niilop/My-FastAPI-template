from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session

from core.config import get_settings
from models.database import DocumentChunk

settings = get_settings()

# Embeddings are always Google text-embedding-004 (768-dim).
# The LLM provider (llm_provider setting) is independent of this choice.
_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=settings.api_key.get_secret_value(),
)

_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)


def ingest_document(db: Session, user_id: int, source: str, text: str) -> int:
    """Chunk, embed, and store a document. Returns number of chunks created."""
    chunks = _splitter.split_text(text)
    if not chunks:
        return 0

    vectors = _embeddings.embed_documents(chunks)

    db.add_all(
        DocumentChunk(user_id=user_id, source=source, content=chunk, embedding=vec)
        for chunk, vec in zip(chunks, vectors)
    )
    db.commit()
    return len(chunks)


def retrieve_chunks(db: Session, user_id: int, query: str, k: int = 4) -> list[DocumentChunk]:
    """Embed the query and return the k nearest chunks via cosine distance."""
    query_vector = _embeddings.embed_query(query)

    return (
        db.query(DocumentChunk)
        .filter(DocumentChunk.user_id == user_id)
        .order_by(DocumentChunk.embedding.cosine_distance(query_vector))
        .limit(k)
        .all()
    )
