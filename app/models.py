from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from typing import Optional
import uuid
import datetime

class Company(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    sector: Optional[str] = None
    stage: Optional[str] = None
    founded_date: Optional[datetime.date] = None
    employees_count: Optional[int] = None
    website: Optional[str] = None
    location: Optional[str] = None

class Founder(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    company_id: uuid.UUID = Field(foreign_key="company.id")
    name: str
    role: Optional[str] = None
    linkedin: Optional[str] = None
    bio: Optional[str] = None
    is_ceo: bool = False

class DealNote(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    company_id: uuid.UUID = Field(foreign_key="company.id")
    summary: Optional[str] = None
    content: Optional[str] = None
    score: Optional[float] = None
    model_version: Optional[str] = None
    generated_by: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class Document(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    company_id: Optional[uuid.UUID] = Field(default=None, foreign_key="company.id")
    filename: str
    storage_path: Optional[str] = None   # e.g., gs://bucket/documents/...
    mime_type: Optional[str] = None
    extracted_json: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    uploaded_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)    
