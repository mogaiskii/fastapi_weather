import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_sanity_db(session: AsyncSession):
    async with session.begin():
        stmt = select(text("'test'"))
        result = await session.execute(stmt)
        value = result.scalars().first()
        assert value == 'test'


@pytest.mark.asyncio
async def test_sanity_app(test_app):
    response = test_app.get("/rest/health")
    assert response.status_code == 200
