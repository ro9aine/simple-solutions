from celery import Celery

from app.core.config import get_settings


settings = get_settings()

celery_app = Celery(
    "deribit_price_service",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
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

celery_app.autodiscover_tasks(["app.tasks"])
