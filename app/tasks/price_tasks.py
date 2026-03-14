import asyncio
from time import time

from app.clients.deribit_client import DeribitClient
from app.core.config import get_settings
from app.core.logging import get_logger
from app.db.session import SessionLocal, init_db
from app.schemas.price import PriceSnapshotCreate
from app.services.price_service import PriceService
from app.tasks.celery_app import celery_app

logger = get_logger(__name__)


async def _collect_prices() -> None:
    settings = get_settings()
    client = DeribitClient(settings.deribit_base_url)
    timestamp = int(time())

    logger.info("Starting price collection for %s tickers", len(settings.default_tickers))
    init_db()
    with SessionLocal() as session:
        service = PriceService(session)
        for ticker in settings.default_tickers:
            try:
                price = await client.get_index_price(ticker)
                service.save_price(
                    PriceSnapshotCreate(
                        ticker=ticker,
                        price=price,
                        timestamp=timestamp,
                    )
                )
                logger.info(
                    "Saved price snapshot for %s at %s with value %s",
                    ticker,
                    timestamp,
                    price,
                )
            except Exception:
                logger.exception("Failed to collect price for %s", ticker)
                raise

    logger.info("Completed price collection run at %s", timestamp)


@celery_app.task(name="app.tasks.price_tasks.fetch_prices")
def fetch_prices() -> None:
    logger.info("Executing fetch_prices task")
    asyncio.run(_collect_prices())
