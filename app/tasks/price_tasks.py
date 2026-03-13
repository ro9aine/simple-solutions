import asyncio
from time import time

from app.clients.deribit_client import DeribitClient
from app.core.config import get_settings
from app.db.session import SessionLocal, init_db
from app.schemas.price import PriceSnapshotCreate
from app.services.price_service import PriceService
from app.tasks.celery_app import celery_app


async def _collect_prices() -> None:
    settings = get_settings()
    client = DeribitClient(settings.deribit_base_url)
    timestamp = int(time())

    init_db()
    with SessionLocal() as session:
        service = PriceService(session)
        for ticker in settings.default_tickers:
            price = await client.get_index_price(ticker)
            service.save_price(
                PriceSnapshotCreate(
                    ticker=ticker,
                    price=price,
                    timestamp=timestamp,
                )
            )


@celery_app.task(name="app.tasks.price_tasks.fetch_prices")
def fetch_prices() -> None:
    asyncio.run(_collect_prices())
