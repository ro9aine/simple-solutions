from celery import Celery

from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger


settings = get_settings()
configure_logging(settings.log_level)
logger = get_logger(__name__)

celery_app = Celery(
    "deribit_price_service",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks.price_tasks"],
)

celery_app.conf.update(
    timezone="UTC",
    beat_schedule={
        "fetch-index-prices-every-minute": {
            "task": "app.tasks.price_tasks.fetch_prices",
            "schedule": 60.0,
        }
    },
)

logger.info("Celery app configured with broker %s", settings.celery_broker_url)
