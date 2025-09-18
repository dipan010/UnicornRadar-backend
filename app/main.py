from fastapi import FastAPI
from app.routes import companies

app = FastAPI(title="Investor Backend")

app.include_router(companies.router)

@app.get("/")
async def root():
    return {"message": "Investor API running"}
