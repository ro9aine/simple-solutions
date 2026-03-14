from decimal import Decimal

import aiohttp
from aiohttp import ClientTimeout


class DeribitClient:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")

    async def get_index_price(self, ticker: str) -> Decimal:
        instrument = ticker.lower()
        url = f"{self._base_url}/public/get_index_price"
        params = {"index_name": instrument}
        timeout = ClientTimeout(total=10)

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=timeout) as response:
                response.raise_for_status()
                payload = await response.json()

        result = payload.get("result")
        if not result or "index_price" not in result:
            raise ValueError(f"Unexpected Deribit response for {ticker}: {payload}")

        return Decimal(str(result["index_price"]))
