from typing import TYPE_CHECKING, List, Union

from naver_finance.synchronous import SymbolService
from naver_finance.interfaces.common.sync_service import SyncService
from naver_finance.utils import parse_EUC_KR

if TYPE_CHECKING:
    from naver_finance.models import Symbol


class SyncSymbolService(SymbolService, SyncService):
    def code_to_name(self, code: str) -> str:
        html = self._fetch(f"/item/main.naver?code={code}")
        soup = self.make_soup(html)
        name = soup.select_one(".h_company > .wrap_company > h2")
        return name.text

    def _get_page_size(self, name: str) -> int:
        html = self._fetch(f"/search/searchList.naver?query={name}")
        soup = self.make_soup(html)
        paging = soup.select_one("#content > .section_search > .paging")
        return len(paging.find_all("a"))

    def name_to_code_list(self, name: str) -> List["Symbol"]:
        stocks: List["Symbol"] = []
        name = parse_EUC_KR(name)
        size = self._get_page_size(name)
        urls = [
            f"/search/searchList.naver?query={name}&page={i + 1}" for i in range(size)
        ]
        htmls = [self._fetch(url) for url in urls]

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

    def get_current_price_by_code(self, code: str) -> Union[int, float]:
        html = self._fetch(f"/item/main.naver?code={code}")
        soup = self.make_soup(html)
        price = soup.select_one("#chart_area > div.rate_info > div > p.no_today > em")
        return int("".join(price.text.split("\n")[1].split(",")))
