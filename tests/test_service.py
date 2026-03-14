from tests.conftest import run_async

from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.price import PriceSnapshotCreate
from app.services.price_service import PriceService


def test_get_latest_price_returns_none_for_missing_ticker(session: AsyncSession) -> None:
    service = PriceService(session)

    latest = run_async(service.get_latest_price("BTC_USD"))

    assert latest is None


def test_save_price_persists_record(session: AsyncSession) -> None:
    service = PriceService(session)

    result = run_async(
        service.save_price(
            PriceSnapshotCreate(
                ticker="ETH_USD",
                price=Decimal("2000.55"),
                timestamp=1700000000,
            )
        )
    )

    assert result.ticker == "ETH_USD"
    assert result.price == Decimal("2000.55000000")
    assert result.timestamp == 1700000000


def test_get_latest_price_returns_most_recent_record(session: AsyncSession) -> None:
    service = PriceService(session)
    run_async(
        service.save_price(
            PriceSnapshotCreate(
                ticker="BTC_USD",
                price=Decimal("40000.12"),
                timestamp=1700000000,
            )
        )
    )
    run_async(
        service.save_price(
            PriceSnapshotCreate(
                ticker="BTC_USD",
                price=Decimal("41000.34"),
                timestamp=1700000060,
            )
        )
    )

    latest = run_async(service.get_latest_price("BTC_USD"))

    assert latest is not None
    assert latest.price == Decimal("41000.34000000")
    assert latest.timestamp == 1700000060
