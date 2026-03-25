# backend/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from api.endpoints import example, llm
from core.config import Settings, get_settings
from core.rate_limit import limiter

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
    allow_methods=["GET", "POST"], # Restrict to only the methods you actually use
    allow_headers=["*"], # Can be restricted further to ["Authorization", "Content-Type", "X-API-Key"]
)

# Include routes
app.include_router(example.router)
app.include_router(llm.router)

# Root endpoint
@app.get("/")
def root(settings: Settings = Depends(get_settings)):
    """
    Returns a basic health message.
    
    NOTE: We use Depends(get_settings) here instead of the global 'settings' 
    variable to allow for 'dependency_overrides' during testing. 
    This lets us inject mock settings (e.g., fake API keys) without 
    changing the application code.
    """
    return {"message": f"{settings.app_name} is running"}

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return {"uptime": "todo", "requests": 0}