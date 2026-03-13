from decimal import Decimal

from pydantic import BaseModel, Field


class PriceSnapshotCreate(BaseModel):
    ticker: str = Field(min_length=3, max_length=16)
    price: Decimal
    timestamp: int = Field(ge=0)


class PriceSnapshotRead(BaseModel):
    ticker: str
    price: Decimal
    timestamp: int

    model_config = {"from_attributes": True}
