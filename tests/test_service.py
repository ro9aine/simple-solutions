from decimal import Decimal

from app.schemas.price import PriceSnapshotCreate
from app.services.price_service import PriceService


def test_get_latest_price_returns_none_for_missing_ticker(session) -> None:
    service = PriceService(session)

    latest = service.get_latest_price("BTC_USD")

    assert latest is None


def test_save_price_persists_record(session) -> None:
    service = PriceService(session)

    result = service.save_price(
        PriceSnapshotCreate(
            ticker="ETH_USD",
            price=Decimal("2000.55"),
            timestamp=1700000000,
        )
    )

    assert result.ticker == "ETH_USD"
    assert result.price == Decimal("2000.55000000")
    assert result.timestamp == 1700000000
