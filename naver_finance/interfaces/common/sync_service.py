from httpx import Client

from naver_finance.interfaces.common.service import Service
from naver_finance.config.constants import BASE_URL


class SyncService(Service):
    def __init__(self) -> None:
        self.http_client = self._client = Client(base_url=BASE_URL)

    def close(self) -> None:
        self._client.close()

    def _fetch(self, url: str) -> str:
        return self.http_client.get(url).text
