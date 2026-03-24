from fastapi import APIRouter, HTTPException
from models.schemas import SummaryRequest, SummaryResponse
from services.llm_service import summarize_text

router = APIRouter(prefix="/llm", tags=["AI Solutions"])

@router.post("/summarize", response_model=SummaryResponse)
def run_summarization(request: SummaryRequest):
    try:
        result = summarize_text(request.text)
        return SummaryResponse(summary=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))