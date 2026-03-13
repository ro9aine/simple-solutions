from sqlalchemy import Select, desc, select
from sqlalchemy.orm import Session

from app.models.price_snapshot import PriceSnapshot
from app.schemas.price import PriceSnapshotCreate


class PriceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, payload: PriceSnapshotCreate) -> PriceSnapshot:
        snapshot = PriceSnapshot(**payload.model_dump())
        self._session.add(snapshot)
        self._session.commit()
        self._session.refresh(snapshot)
        return snapshot

    def get_all_by_ticker(self, ticker: str) -> list[PriceSnapshot]:
        statement = self._base_ticker_query(ticker)
        return list(self._session.scalars(statement))

    def get_latest_by_ticker(self, ticker: str) -> PriceSnapshot | None:
        statement = self._base_ticker_query(ticker).order_by(desc(PriceSnapshot.timestamp)).limit(1)
        return self._session.scalar(statement)

    def get_by_ticker_and_date_range(
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
        return list(self._session.scalars(statement))

    @staticmethod
    def _base_ticker_query(ticker: str) -> Select[tuple[PriceSnapshot]]:
        return (
            select(PriceSnapshot)
            .where(PriceSnapshot.ticker == ticker.upper())
            .order_by(PriceSnapshot.timestamp)
        )
