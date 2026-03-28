# backend/api/endpoints/data.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from models.schemas import DataCatalogResponse
from core.database import get_db
from services.auth_service import  decode_token, get_user_by_email
from services.data_service import process_and_save_dataset, get_user_datasets
from api.endpoints.auth import oauth2_scheme
from typing import List
import shutil
import os

router = APIRouter(prefix="/data", tags=["Data Catalog"])

@router.post("/upload")
async def upload_data(
    name: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    # Auth Check
    token_data = decode_token(token)
    user = get_user_by_email(db, token_data["email"])
    
    # Save physical file
    file_location = f"data/raw/{file.filename}"
    os.makedirs("data/raw", exist_ok=True)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process and Catalog
    try:
        catalog_entry = process_and_save_dataset(
            db, user.id, file_location, name, description
        )
        return catalog_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process data: {str(e)}")
    

@router.get("/", response_model=List[DataCatalogResponse])
def list_datasets(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """Get all datasets for the authenticated user."""
    # Auth Check
    token_data = decode_token(token)
    user = get_user_by_email(db, token_data["email"])
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch datasets
    datasets = get_user_datasets(db, user.id)
    return datasets