from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any, AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import get_settings


class PgStorage:
    _instance = None

    def __init__(self, pg_dsn: Optional[str] = None) -> None:
        self.pg_dsn = pg_dsn if pg_dsn else get_settings().postgres_dsn
        self.pg_engine = create_async_engine(self.pg_dsn)
        self.pg_sessionmaker = async_sessionmaker(
            self.pg_engine, expire_on_commit=False
        )

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.pg_sessionmaker() as session:
            yield session

    async def close(self) -> None:
        await self.pg_engine.dispose()

    # === Do your stuff here ===

    ...


@lru_cache
def get_pg_storage() -> PgStorage:
    return PgStorage()
