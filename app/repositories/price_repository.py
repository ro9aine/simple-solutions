from sqlalchemy import Select, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.price_snapshot import PriceSnapshot
from app.schemas.price import PriceSnapshotCreate


class PriceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, payload: PriceSnapshotCreate) -> PriceSnapshot:
        snapshot = PriceSnapshot(**payload.model_dump())
        self._session.add(snapshot)
        await self._session.commit()
        await self._session.refresh(snapshot)
        return snapshot

    async def get_all_by_ticker(self, ticker: str) -> list[PriceSnapshot]:
        statement = self._base_ticker_query(ticker)
        return list(await self._session.scalars(statement))

    async def get_latest_by_ticker(self, ticker: str) -> PriceSnapshot | None:
        statement = (
            self._base_ticker_query(ticker)
            .order_by(None)
            .order_by(desc(PriceSnapshot.timestamp))
            .limit(1)
        )
        return await self._session.scalar(statement)

    async def get_by_ticker_and_date_range(
        self,
        ticker: str,
        start_timestamp: int | None,
        end_timestamp: int | None,
    ) -> list[PriceSnapshot]:
        statement = self._base_ticker_query(ticker)
        if start_timestamp is not None:
            statement = statement.where(PriceSnapshot.timestamp >= start_timestamp)
        if end_timestamp is not None:
            statement = statement.where(PriceSnapshot.timestamp <= end_timestamp)
        return list(await self._session.scalars(statement))

    @staticmethod
    def _base_ticker_query(ticker: str) -> Select[tuple[PriceSnapshot]]:
        return (
            select(PriceSnapshot)
            .where(PriceSnapshot.ticker == ticker.upper())
            .order_by(PriceSnapshot.timestamp)
        )
