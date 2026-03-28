# backend/main.py
from fastapi import FastAPI, Depends, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import Optional
from api.endpoints import example, llm, auth, data
from core.config import Settings, get_settings
from core.rate_limit import limiter
from core.database import Base, engine
from services.auth_service import decode_token, get_user_by_email
from core.database import get_db
from sqlalchemy.orm import Session

# Create all database tables
# Base.metadata.create_all(bind=engine)

# Load settings once at startup
settings = get_settings()

app = FastAPI(title="DS POC API")

# Register the limiter to the FastAPI app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings.cors_origins,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


def verify_token(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """Extract and verify JWT token from Authorization header."""
    if not authorization:
        return None
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        return decode_token(token)
    except (ValueError, IndexError):
        return None


# Include routes
app.include_router(auth.router)
app.include_router(example.router)
app.include_router(llm.router)
app.include_router(data.router)

# Root endpoint
@app.get("/")
def root(settings: Settings = Depends(get_settings)):
    """Returns a basic health message."""
    return {"message": f"{settings.app_name} is running"}


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return {"uptime": "todo", "requests": 0}