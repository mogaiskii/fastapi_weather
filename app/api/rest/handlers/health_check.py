from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.rest import rest_app
from app import get_db


@rest_app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    return {"status": "OK"}
