from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_price_service
from app.db.base import Base
from app.main import app
from app.services.price_service import PriceService


@pytest.fixture()
def session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(session: Session, monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    def override_service() -> Generator[PriceService, None, None]:
        yield PriceService(session)

    monkeypatch.setattr("app.main.init_db", lambda: None)
    app.dependency_overrides[get_price_service] = override_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
