import asyncio
from collections.abc import Generator
from collections.abc import AsyncGenerator, Coroutine
from typing import Any, TypeVar

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_price_service
from app.db.base import Base
from app.main import app
from app.services.price_service import PriceService


T = TypeVar("T")


def run_async(awaitable: Coroutine[Any, Any, T]) -> T:
    return asyncio.run(awaitable)


@pytest.fixture()
def session() -> Generator[AsyncSession, None, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    )

    async def init_models() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def drop_models() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)

    run_async(init_models())
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        run_async(db_session.close())
        run_async(drop_models())
        run_async(engine.dispose())


@pytest.fixture()
def client(
    session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[TestClient, None, None]:
    async def override_service() -> AsyncGenerator[PriceService, None]:
        yield PriceService(session)

    async def noop_init_db() -> None:
        return None

    monkeypatch.setattr("app.main.init_db", noop_init_db)
    app.dependency_overrides[get_price_service] = override_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
