import asyncio
from app.db import AsyncSessionLocal, init_db
from app.models import Company

async def seed():
    await init_db()
    async with AsyncSessionLocal() as session:
        c = Company(name="Test Startup", slug="test-startup", description="Demo company")
        session.add(c)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())
