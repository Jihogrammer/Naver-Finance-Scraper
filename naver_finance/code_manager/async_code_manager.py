from argparse import ArgumentError
import asyncio
import atexit
from typing import TYPE_CHECKING, Optional, List, Union
from urllib import parse

from naver_finance.code_manager import CodeManager
from naver_finance.service import AsyncService

if TYPE_CHECKING:
    from naver_finance.models import Stock


class __AsyncCodeManager(CodeManager, AsyncService):
    async def code_to_name(self, code: str) -> Optional[str]:
        response = await self._client.get(f"/item/main.naver?code={code}")
        soup = self.make_soup(response.text)
        name = soup.select_one(".h_company > .wrap_company > h2")

        try:
            return name.text
        except AttributeError:
            return None

    async def name_to_code_list(self, name: str) -> List["Stock"]:
        stocks: List["Stock"] = []
        name = parse.quote(name, encoding="euc-kr")

        async def get_page_size(name: str) -> int:
            response = await self._client.get(f"/search/searchList.naver?query={name}")
            soup = self.make_soup(response.text)
            paging = soup.select_one("#content > .section_search > .paging")

            try:
                return len(paging.find_all("a"))
            except AttributeError:
                return 0

        async def fetch(url: str):
            response = await self._client.get(url)
            return response.text

        size = await get_page_size(name)
        urls = [
            f"/search/searchList.naver?query={name}&page={i + 1}" for i in range(size)
        ]
        htmls = await asyncio.gather(*[fetch(url) for url in urls])

        for html in htmls:
            soup = self.make_soup(html)
            stock_elements = soup.select(
                "#content > div.section_search > table > tbody > tr"
            )

            for element in stock_elements:
                stock = element.select_one("td.tit > a")
                name = stock.text
                code = stock.attrs["href"].split("=")[-1]
                stocks.append({"name": name, "code": code})

        return stocks

    async def get_current_price_by_code(self, code: str) -> Union[int, float]:
        response = await self._client.get(f"/item/main.naver?code={code}")
        soup = self.make_soup(response.text)
        price = soup.select_one("#chart_area > div.rate_info > div > p.no_today > em")
        try:
            return int("".join(price.text.split("\n")[1].split(",")))
        except:
            raise ArgumentError(None, f"(received code = {code}) 코드를 다시 한 번 확인해주세요.")


code_manager = __AsyncCodeManager()


@atexit.register
def __close():
    asyncio.run(code_manager.close())
