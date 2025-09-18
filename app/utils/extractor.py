# app/utils/extractors.py
import os
from tempfile import NamedTemporaryFile
from pdfminer.high_level import extract_text
from docx import Document as DocxDocument

def extract_from_pdf_bytes(b: bytes) -> dict:
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(b)
        tmp.flush()
        path = tmp.name
    try:
        text = extract_text(path) or ""
        return {"text": text}
    finally:
        try:
            os.unlink(path)
        except:
            pass

def extract_from_docx_bytes(b: bytes) -> dict:
    with NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(b)
        tmp.flush()
        path = tmp.name
    try:
        doc = DocxDocument(path)
        paras = [p.text for p in doc.paragraphs if p.text]
        return {"text": "\n\n".join(paras)}
    finally:
        try:
            os.unlink(path)
        except:
            pass

def extract_from_bytes_guess(b: bytes, filename: str = "") -> dict:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_from_pdf_bytes(b)
    if lower.endswith(".docx") or lower.endswith(".doc"):
        return extract_from_docx_bytes(b)
    # fallback: try utf-8 decode
    try:
        text = b.decode("utf-8", errors="ignore")
        return {"text": text}
    except:
        return {"text": ""}
