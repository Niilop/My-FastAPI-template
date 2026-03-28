# backend/api/endpoints/data.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from requests import Session
from models.schemas import DataCatalogResponse
from core.database import get_db
from services.auth_service import  decode_token, get_user_by_email
from services.data_service import process_and_save_dataset, get_user_datasets, count_user_datasets
from api.endpoints.auth import oauth2_scheme
from typing import List
import shutil
import os

router = APIRouter(prefix="/data", tags=["Data Catalog"])

# Define the maximum file size (10 MB in bytes)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Update your upload endpoint
@router.post("/upload")
async def upload_data(
    name: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    # 1. Auth Check
    token_data = decode_token(token)
    user = get_user_by_email(db, token_data["email"])
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Limit Check: Enforce maximum of 10 datasets
    current_count = count_user_datasets(db, user.id)
    if current_count >= 10:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Storage limit reached. You can only upload a maximum of 10 datasets."
        )

    # 3. Limit Check: Enforce file size limit (10MB)
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds the 10MB limit. Your file is {file.size / (1024 * 1024):.2f}MB."
        )
    
    # 4. Save physical file
    file_location = f"data/raw/{file.filename}"
    os.makedirs("data/raw", exist_ok=True)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 5. Process and Catalog
    try:
        catalog_entry = process_and_save_dataset(
            db, user.id, file_location, name, description
        )
        return catalog_entry
    except Exception as e:
        # Cleanup file if processing fails
        if os.path.exists(file_location):
            os.remove(file_location)
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

@router.get("/count")
def get_dataset_count(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """Get the total number of datasets uploaded by the authenticated user."""
    # 1. Auth Check
    token_data = decode_token(token)
    user = get_user_by_email(db, token_data["email"])
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Fetch Count
    count = count_user_datasets(db, user.id)
    
    # 3. Return count and the maximum limit for frontend convenience
    return {
        "count": count,
        "limit": 10,
        "remaining": 10 - count
    }