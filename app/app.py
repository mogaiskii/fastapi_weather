from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from db.main import make_connection, get_sessionmaker, destroy_connection
from settings import settings

app = FastAPI()


db = make_connection(settings)
SessionMaker = get_sessionmaker(db)


async def get_db() -> AsyncSession:
    async with SessionMaker() as session:
        try:
            yield session
        finally:
            await session.close()


@app.on_event("shutdown")
async def close_connection():
    destroy_connection(db)
