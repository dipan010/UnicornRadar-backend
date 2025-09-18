from pydantic import BaseModel
from typing import Optional
import uuid
import datetime

class CompanyBase(BaseModel):
    name: str
    slug: Optional[str]
    description: Optional[str]
    sector: Optional[str]
    stage: Optional[str]

class CompanyRead(CompanyBase):
    id: uuid.UUID

class DealNoteRead(BaseModel):
    id: uuid.UUID
    summary: Optional[str]
    content: Optional[str]
    score: Optional[float]
    created_at: datetime.datetime
