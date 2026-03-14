from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router as prices_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.db.session import init_db

settings = get_settings()
configure_logging(settings.log_level)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Initializing application database")
    init_db()
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown complete")


app = FastAPI(
    title="Deribit Price Service",
    description="API for querying stored Deribit index prices.",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(prices_router)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
