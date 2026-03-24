# backend/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import example, llm
from core.config import Settings, get_settings

app = FastAPI(title="DS POC API")

# Configure CORS middleware
origins = [
    "http://localhost",
    "http://localhost:8501", # Allow your Streamlit frontend
    "http://localhost:3000", # Common for React/Vue
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
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