from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker, AsyncSession,
)
from contextlib import asynccontextmanager

from app.config import settings


class Database:

    def __init__(self) -> None:
        self.__engine = create_async_engine(
            url=settings.DB_URL
        )
        self.__session_maker = async_sessionmaker(
            bind=self.__engine,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session_factory(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.__session_maker() as session:
            yield session

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession | None = None
        try:
            async with self.session_factory() as session:
                yield session
        except Exception as e:
            if session:
                await session.rollback()
                raise e


db = Database()
