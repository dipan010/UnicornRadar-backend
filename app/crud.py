from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from sqlmodel import select
from .models import Company, DealNote, Document

async def get_companies(session: AsyncSession):
    result = await session.execute(select(Company))
    return result.scalars().all()

async def get_company(session: AsyncSession, company_id: str):
    result = await session.execute(select(Company).where(Company.id == company_id))
    return result.scalar_one_or_none()

async def get_deal_notes(session: AsyncSession, company_id: str):
    result = await session.execute(select(DealNote).where(DealNote.company_id == company_id))
    return result.scalars().all()

async def create_document(session: AsyncSession, filename: str, storage_path: str, mime_type: str, company_id: Optional[str] = None) -> Document:
    doc = Document(filename=filename, storage_path=storage_path, mime_type=mime_type, company_id=company_id)
    session.add(doc)
    await session.commit()
    await session.refresh(doc)
    return doc

async def update_document_extracted(session: AsyncSession, doc_id: str, extracted_json: dict):
    result = await session.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        return None
    doc.extracted_json = extracted_json
    session.add(doc)
    await session.commit()
    await session.refresh(doc)
    return doc

async def get_document(session: AsyncSession, doc_id: str):
    result = await session.execute(select(Document).where(Document.id == doc_id))
    return result.scalar_one_or_none()
