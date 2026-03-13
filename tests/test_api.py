from decimal import Decimal

from app.schemas.price import PriceSnapshotCreate
from app.services.price_service import PriceService


def seed_prices(service: PriceService) -> None:
    service.save_price(PriceSnapshotCreate(ticker="BTC_USD", price=Decimal("40000.12"), timestamp=1700000000))
    service.save_price(PriceSnapshotCreate(ticker="BTC_USD", price=Decimal("41000.34"), timestamp=1700000060))
    service.save_price(PriceSnapshotCreate(ticker="ETH_USD", price=Decimal("2500.11"), timestamp=1700000120))


def test_get_all_prices(client, session) -> None:
    seed_prices(PriceService(session))

    response = client.get("/prices", params={"ticker": "BTC_USD"})

    assert response.status_code == 200
    assert response.json() == [
        {"ticker": "BTC_USD", "price": "40000.12000000", "timestamp": 1700000000},
        {"ticker": "BTC_USD", "price": "41000.34000000", "timestamp": 1700000060},
    ]


def test_get_latest_price(client, session) -> None:
    seed_prices(PriceService(session))

    response = client.get("/prices/latest", params={"ticker": "BTC_USD"})

    assert response.status_code == 200
    assert response.json() == {
        "ticker": "BTC_USD",
        "price": "41000.34000000",
        "timestamp": 1700000060,
    }


def test_get_prices_by_date(client, session) -> None:
    seed_prices(PriceService(session))

    response = client.get(
        "/prices/by-date",
        params={
            "ticker": "BTC_USD",
            "start_timestamp": 1700000030,
            "end_timestamp": 1700000090,
        },
    )

    assert response.status_code == 200
    assert response.json() == [
        {"ticker": "BTC_USD", "price": "41000.34000000", "timestamp": 1700000060},
    ]


def test_get_prices_by_date_requires_range(client) -> None:
    response = client.get("/prices/by-date", params={"ticker": "BTC_USD"})

    assert response.status_code == 400
