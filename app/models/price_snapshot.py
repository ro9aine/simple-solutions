from decimal import Decimal

from sqlalchemy import BigInteger, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"
    __table_args__ = (
        Index("ix_price_snapshots_ticker_timestamp", "ticker", "timestamp"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
