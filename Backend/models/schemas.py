from pydantic import BaseModel
from typing import List, Optional

# backend/models/schemas.py
from pydantic import BaseModel

class ExampleRequest(BaseModel):
    name: str
    task: str

class ExampleResponse(BaseModel):
    result: str

# NEW AI Models
class SummaryRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str