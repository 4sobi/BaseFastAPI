from typing import Any, Generic, List, Optional, TypeVar, get_args

from pydantic import BaseModel
from sqlalchemy import select, update, delete

from db.session import session


Domain = TypeVar("Domain")
Model = TypeVar("Model", bound=BaseModel)


class BaseRepository(Generic[Domain, Model]):

    @classmethod
    async def create(cls, data: Model) -> Model:
        newer = Domain(**data.model_dump(by_alias=True, exclude_none=True))
        session.add(newer)
        await session.flush()
        return Model.model_validate(newer)

    @classmethod
    async def create_all(cls, datas: List[Model]) -> List[Model]:
        newer_list = [
            Domain(**data.model_dump(by_alias=True, exclude_none=True))
            for data in datas
        ]
        session.add_all(newer_list)
        await session.flush()
        return [Model.model_validate(i) for i in newer_list]

    @classmethod
    async def find(
        cls, conds: List, orders: Optional[List] = None, offset: int = 0, limit: int = 0
    ) -> List[Model]:
        stmt = select(Domain)
        for cond in conds:
            stmt = stmt.where(cond)

        if orders:
            stmt = stmt.order_by(*orders)
        else:
            stmt = stmt.order_by(
                *list(map(lambda x: x.desc(), Domain.__table__.primary_key.columns))
            )

        if limit:
            stmt = stmt.offset(offset * limit).limit(limit)

        result = (await session.scalars(stmt)).all()
        return [Model.model_validate(i) for i in result]

    @classmethod
    async def find_one(cls, conds: List) -> Optional[Model]:
        result = await cls.find(conds)
        if len(result) == 1:
            return result[0]
        return None

    @classmethod
    async def find_by_id(cls, key: Any) -> Optional[Model]:
        result = await session.get(Domain, key)

        if result:
            return Model.model_validate(result)
        return None

    @classmethod
    async def update(
            cls,
            conds: List,
            values: dict,
            returning_cols: List = [],
    ):
        domain = Domain
        stmt = update(domain)
        for cond in conds:
            stmt = stmt.where(cond)
        stmt = stmt.values(values)

        if returning_cols:
            stmt = stmt.returning(*returning_cols)
            
        return await cls.execute(stmt)

    @classmethod
    async def delete(cls, conds: List):
        domain = Domain
        stmt = delete(domain)
        for cond in conds:
            stmt = stmt.where(cond)

        return await cls.execute(stmt)

    @classmethod
    async def execute(cls, stmt):
        result = await session.execute(stmt)
        await session.flush()
        return result
