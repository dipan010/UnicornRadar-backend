from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import AsyncSessionLocal
from app import crud

router = APIRouter()

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/companies")
async def list_companies(session: AsyncSession = Depends(get_session)):
    return await crud.get_companies(session)

@router.get("/companies/{company_id}")
async def get_company(company_id: str, session: AsyncSession = Depends(get_session)):
    company = await crud.get_company(session, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
