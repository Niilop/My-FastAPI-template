# backend/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from api.endpoints import example, llm
from core.config import Settings, get_settings

# Initialize the rate limiter
# get_remote_address uses the IP address of the incoming request
limiter = Limiter(key_func=get_remote_address)


app = FastAPI(title="DS POC API")

# Register the limiter to the FastAPI app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS middleware
origins = [
    "http://localhost:8501",   # Active: Streamlit frontend
    "http://127.0.0.1:8501",   # Active: Streamlit frontend (IP format)
    
    # FUTURE REACT FRONTEND PORTS:
    # "http://localhost:3000", # Inactive: Standard Create React App port
    # "http://localhost:5173", # Inactive: Modern React (Vite) port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"], # Restrict to only the methods you actually use
    allow_headers=["*"], # Can be restricted further to ["Authorization", "Content-Type", "X-API-Key"]
)

# Include routes
app.include_router(example.router)
app.include_router(llm.router)

# Root endpoint
@app.get("/")
def root(settings: Settings = Depends(get_settings)):
    return {"message": f"{settings.app_name} is running"}

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return {"uptime": "todo", "requests": 0}