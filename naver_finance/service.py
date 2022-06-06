from abc import ABCMeta, abstractmethod

from httpx import Client, AsyncClient, Response
from bs4 import BeautifulSoup

from naver_finance.config.constants import BASE_URL


class __Service(metaclass=ABCMeta):
    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def _fetch(self, url: str) -> str:
        pass

    def make_soup(self, html: str) -> "BeautifulSoup":
        return BeautifulSoup(html, "html.parser")


class SyncService(__Service):
    def __init__(self) -> None:
        self._client = Client(base_url=BASE_URL)

    def _fetch(self, url: str) -> str:
        return self._client.get(url).text

    def close(self) -> None:
        self._client.close()


class AsyncService(__Service):
    def __init__(self) -> None:
        self._client = AsyncClient(base_url=BASE_URL)

    async def _fetch(self, url: str) -> str:
        response = await self._client.get(url)
        return response.text

    async def close(self) -> None:
        await self._client.aclose()
