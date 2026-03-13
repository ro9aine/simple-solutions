from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.services.price_service import PriceService


def get_price_service(session: Session = Depends(get_db_session)) -> Generator[PriceService, None, None]:
    yield PriceService(session)
