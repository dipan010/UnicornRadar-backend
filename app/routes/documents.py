# app/routes/documents.py
import os
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from google.cloud import storage
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import AsyncSessionLocal
from app import crud
from app.utils.extractors import extract_from_bytes_guess

router = APIRouter()

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

def upload_bytes_to_gcs(bucket_name: str, blob_name: str, data: bytes, content_type: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data, content_type=content_type)
    return f"gs://{bucket_name}/{blob_name}"

def _extract_and_save_task(doc_id: str, storage_path: str, filename: str):
    # runs in background (synchronous). Downloads from GCS and extracts, then writes DB via sync wrapper
    client = storage.Client()
    # storage_path = gs://bucket/path... -> split
    _, rest = storage_path.split("gs://", 1)
    bucket_name, _, blob_path = rest.partition("/")
    blob = client.bucket(bucket_name).blob(blob_path)
    content = blob.download_as_bytes()
    extracted = extract_from_bytes_guess(content, filename=filename)

    # we need an async DB session to update record; use sync->async trick:
    import asyncio
    from app.db import AsyncSessionLocal
    from app.models import Document, DealNote
    async def _update():
        async with AsyncSessionLocal() as session:
            await crud.update_document_extracted(session, doc_id, extracted)
            # optional: create a cheap auto-deal-note stub
            # summarize first 500 chars as summary
            text = extracted.get("text","")
            summary = (text[:500] + "...") if len(text) > 500 else text
            if summary.strip():
                from app.models import DealNote
                dn = DealNote(company_id=None, summary=summary, content=text[:4000])
                session.add(dn)
                await session.commit()
    asyncio.run(_update())

@router.post("/documents/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    company_id: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    # Basic validation
    if file.content_type not in ("application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain", "application/msword"):
        # allow more if you want
        raise HTTPException(status_code=400, detail=f"unsupported content-type: {file.content_type}")

    data = await file.read()
    bucket_name = os.getenv("GCS_BUCKET")
    if not bucket_name:
        raise HTTPException(status_code=500, detail="GCS_BUCKET env not set")

    blob_name = f"documents/{uuid4().hex}_{file.filename}"
    # Upload synchronously (blocking) — OK for small loads; optimize later
    storage_path = upload_bytes_to_gcs(bucket_name, blob_name, data, file.content_type)

    # create DB record
    doc = await crud.create_document(session, filename=file.filename, storage_path=storage_path, mime_type=file.content_type, company_id=company_id)

    # background extraction & optional dealnote creation
    background_tasks.add_task(_extract_and_save_task, str(doc.id), storage_path, file.filename)

    return {"id": str(doc.id), "storage_path": storage_path}
