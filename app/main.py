from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router as prices_router
from app.db.session import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


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
