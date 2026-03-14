from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.services.price_service import PriceService


async def get_price_service(
    session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[PriceService, None]:
    yield PriceService(session)
