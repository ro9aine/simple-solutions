from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_price_service
from app.schemas.price import PriceSnapshotRead
from app.services.price_service import PriceService


router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("", response_model=list[PriceSnapshotRead])
def get_prices(
    ticker: str = Query(..., min_length=3, max_length=16),
    service: PriceService = Depends(get_price_service),
) -> list[PriceSnapshotRead]:
    return service.get_prices(ticker)


@router.get("/latest", response_model=PriceSnapshotRead)
def get_latest_price(
    ticker: str = Query(..., min_length=3, max_length=16),
    service: PriceService = Depends(get_price_service),
) -> PriceSnapshotRead:
    latest = service.get_latest_price(ticker)
    if latest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No price data found for ticker '{ticker.upper()}'.",
        )
    return latest


@router.get("/by-date", response_model=list[PriceSnapshotRead])
def get_prices_by_date(
    ticker: str = Query(..., min_length=3, max_length=16),
    start_timestamp: int | None = Query(default=None, ge=0),
    end_timestamp: int | None = Query(default=None, ge=0),
    service: PriceService = Depends(get_price_service),
) -> list[PriceSnapshotRead]:
    if start_timestamp is None and end_timestamp is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one of start_timestamp or end_timestamp must be provided.",
        )

    if (
        start_timestamp is not None
        and end_timestamp is not None
        and start_timestamp > end_timestamp
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_timestamp must be less than or equal to end_timestamp.",
        )

    return service.get_prices_by_date(ticker, start_timestamp, end_timestamp)
