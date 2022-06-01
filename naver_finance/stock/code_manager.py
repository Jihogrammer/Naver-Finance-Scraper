from typing import TYPE_CHECKING, List, Union
import requests
from urllib import parse
from bs4 import BeautifulSoup


if TYPE_CHECKING:
    from naver_finance.models.stock import Stock


def code_to_name(code: str):

    response = requests.get(f"https://finance.naver.com/item/main.naver?code={code}")
    soup = BeautifulSoup(response.text, "html.parser")
    name = soup.select_one(".h_company > .wrap_company > h2")

    try:
        return name.text
    except AttributeError:
        return None


def __get_page_size(name: str) -> int:
    response = requests.get(
        f"https://finance.naver.com/search/searchList.naver?query={name}"
    )
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        return len(
            soup.select_one("#content > .section_search > .paging").find_all("a")
        )
    except AttributeError:
        return 0


def name_to_code_list(name: str) -> List["Stock"]:
    list: List["Stock"] = []
    name = parse.quote(name, encoding="euc-kr")

    for i in range(__get_page_size(name)):
        response = requests.get(
            f"https://finance.naver.com/search/searchList.naver?query={name}&page={i + 1}"
        )
        soup = BeautifulSoup(response.text, "html.parser")
        stocks = soup.select("#content > div.section_search > table > tbody > tr")

        for element in stocks:
            stock = element.select_one("td.tit > a")
            name = stock.text
            code = stock.attrs["href"].split("=")[-1]
            list.append({"name": name, "code": code})

    return list


def get_current_price_by_code(code: str) -> Union[int, float]:
    response = requests.get(f"https://finance.naver.com/item/main.naver?code={code}")
    soup = BeautifulSoup(response.text, "html.parser")
    price = soup.select_one("#chart_area > div.rate_info > div > p.no_today > em").text
    return int("".join(price.split("\n")[1].split(",")))


if __name__ == "__main__":
    stocks = name_to_code_list("삼성")
    for stock in stocks:
        print(stock["code"], stock["name"], get_current_price_by_code(stock["code"]))
