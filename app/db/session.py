from contextlib import asynccontextmanager
from contextvars import ContextVar, Token

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Delete, Insert, Update

from config.config import DatabaseConfig

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return create_async_engine(DatabaseConfig.db_dsn, pool_recycle=3600).sync_engine
        else:
            return create_async_engine(DatabaseConfig.db_dsn, pool_recycle=3600).sync_engine


_async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
)
session = async_scoped_session(
    session_factory=_async_session_factory,
    scopefunc=get_session_context,
)


def transactional(func):
    async def _transactional(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            await session.commit()
        except Exception as err:
            await session.rollback()
            raise err

        return result

    return _transactional
