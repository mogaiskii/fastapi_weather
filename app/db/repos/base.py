import uuid
from typing import List, Any

from sqlalchemy import select, delete, insert, update, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from db.models import DBModel
from db.repos.exceptions import RepoNotFound, RepoManyForOne


class Repo:
    __model__ = DBModel
    __sorted_by__ = None

    def __init__(self, session: AsyncSession):
        self.session = session

    def build_item(self, **item_kwargs) -> DBModel:
        return self.__model__(**item_kwargs)

    async def create(self, *, flush: bool = True, commit: bool = False, **item_kwargs) -> DBModel:
        item = self.build_item(**item_kwargs)
        return await self.save(item, flush=flush, commit=commit)

    async def save(self, item, *, flush: bool = True, commit: bool = False) -> DBModel:
        self.session.add(item)
        if flush:
            await self.session.flush([item])
        if commit:
            await self.session.commit()

        await self.session.refresh(item)
        return item

    async def delete(self, id: uuid.UUID, *, commit: bool = False):
        statement = delete(self.__model__).where(self.__model__.id == id)
        await self.session.execute(statement)
        if commit:
            await self.session.commit()

    async def update(self, id: uuid.UUID, values: dict[str, Any], *, commit: bool = False) -> None:
        stmt = update(self.__model__).where(self.__model__.id == id).values(**values)
        await self.session.execute(stmt)
        if commit:
            await self.session.commit()

    async def insert(self, values: List[dict[str, Any]], *, commit: bool = False) -> None:
        stmt = insert(self.__model__).values(values)
        await self.session.execute(stmt)
        if commit:
            await self.session.commit()

    async def exists(self, item_id: uuid.UUID) -> bool:
        stmt = select(exists().where(self.__model__.id == item_id))
        result = await self.session.execute(stmt)
        return result.scalar()

    @property
    def query(self) -> Select:
        stmt = select(self.__model__)
        if self.__sorted_by__ is not None:
            stmt = stmt.order_by(self.__sorted_by__)
        return stmt

    async def fetch_one(self, statement: Select) -> DBModel:
        statement = statement.limit(2)
        result = await self.session.execute(statement)
        items = result.unique().scalars().all()
        if len(items) == 0:
            raise RepoNotFound
        if len(items) == 2:
            raise RepoManyForOne
        return items[0]

    async def fetch_many(self, statement: Select, mapper=None) -> List[DBModel]:
        if mapper:
            statement = mapper.patch_statement(statement)

        result = await self.session.execute(statement)
        items = result.unique().scalars().all()
        return items

    async def get_by_id(self, id: uuid.UUID):
        stmt = self.query.where(self.__model__.id == id)
        return await self.fetch_one(stmt)

    async def get_all(self, mapper=None):
        return await self.fetch_many(self.query, mapper=mapper)