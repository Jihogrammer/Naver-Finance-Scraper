from httpx import AsyncClient

from naver_finance.interfaces.common.service import Service
from naver_finance.config.constants import BASE_URL


class AsyncService(Service):
    def __init__(self) -> None:
        self.http_client = AsyncClient(base_url=BASE_URL)

    async def close(self) -> None:
        await self.http_client.aclose()

    async def _fetch(self, url: str) -> str:
        return (await self.http_client.get(url)).text
