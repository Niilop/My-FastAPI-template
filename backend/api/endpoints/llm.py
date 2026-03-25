from fastapi import APIRouter, HTTPException, Request
from models.schemas import SummaryRequest, SummaryResponse
from services.llm_service import summarize_text
from slowapi import Limiter
from slowapi.util import get_remote_address
from core.rate_limit import limiter

router = APIRouter(prefix="/llm", tags=["AI Solutions"])

@router.post("/summarize", response_model=SummaryResponse)
@limiter.limit("5/minute")
def run_summarization(request: Request, body: SummaryRequest):
    try:
        result = summarize_text(body.text)
        return SummaryResponse(summary=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))