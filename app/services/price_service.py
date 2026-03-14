from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.price_repository import PriceRepository
from app.schemas.price import PriceSnapshotCreate, PriceSnapshotRead


class PriceService:
    def __init__(self, session: AsyncSession) -> None:
        self._repository = PriceRepository(session)

    async def save_price(self, payload: PriceSnapshotCreate) -> PriceSnapshotRead:
        return PriceSnapshotRead.model_validate(await self._repository.add(payload))

    async def get_prices(self, ticker: str) -> list[PriceSnapshotRead]:
        rows = await self._repository.get_all_by_ticker(ticker)
        return [PriceSnapshotRead.model_validate(item) for item in rows]

    async def get_latest_price(self, ticker: str) -> PriceSnapshotRead | None:
        latest = await self._repository.get_latest_by_ticker(ticker)
        if latest is None:
            return None
        return PriceSnapshotRead.model_validate(latest)

    async def get_prices_by_date(
        self,
        ticker: str,
        start_timestamp: int | None,
        end_timestamp: int | None,
    ) -> list[PriceSnapshotRead]:
        rows = await self._repository.get_by_ticker_and_date_range(
            ticker=ticker,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )
        return [PriceSnapshotRead.model_validate(item) for item in rows]
