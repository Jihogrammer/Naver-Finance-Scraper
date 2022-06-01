import asyncio
from typing import TYPE_CHECKING, List, Union
import aiohttp
import requests
from urllib import parse
from bs4 import BeautifulSoup


if TYPE_CHECKING:
    from naver_finance.models.stock import Stock


async def code_to_name(code: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://finance.naver.com/item/main.naver?code={code}"
        ) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            name = soup.select_one(".h_company > .wrap_company > h2")

            try:
                return name.text
            except AttributeError:
                return None


async def __get_page_size(session: aiohttp.ClientSession, name: str) -> int:
    response = await session.get(
        f"https://finance.naver.com/search/searchList.naver?query={name}"
    )
    soup = BeautifulSoup(await response.text(), "html.parser")
    paging = soup.select_one("#content > .section_search > .paging")

    try:
        return len(paging.find_all("a"))
    except AttributeError:
        return 0


async def name_to_code_list(name: str) -> List["Stock"]:
    list: List["Stock"] = []
    name = parse.quote(name, encoding="euc-kr")

    async def fetch(session: aiohttp.ClientSession, url: str):
        response = await session.get(url)
        return await response.text()

    async with aiohttp.ClientSession() as session:
        size = await __get_page_size(session, name)

        urls = [
            f"https://finance.naver.com/search/searchList.naver?query={name}&page={i + 1}"
            for i in range(size)
        ]

        htmls = await asyncio.gather(*[fetch(session, url) for url in urls])

        for html in htmls:
            soup = BeautifulSoup(html, "html.parser")
            stocks = soup.select("#content > div.section_search > table > tbody > tr")

            for element in stocks:
                stock = element.select_one("td.tit > a")
                name = stock.text
                code = stock.attrs["href"].split("=")[-1]
                list.append({"name": name, "code": code})

    return list


async def get_current_price_by_code(code: str) -> Union[int, float]:
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"https://finance.naver.com/item/main.naver?code={code}"
        )
        soup = BeautifulSoup(await response.text(), "html.parser")
        price = soup.select_one(
            "#chart_area > div.rate_info > div > p.no_today > em"
        ).text
        return int("".join(price.split("\n")[1].split(",")))


if __name__ == "__main__":
    stocks = name_to_code_list("삼성")
    for stock in stocks:
        print(stock["code"], stock["name"], get_current_price_by_code(stock["code"]))
