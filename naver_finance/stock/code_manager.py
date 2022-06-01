import requests


BASE_URL = "https://finance.naver.com/item/main.naver"


def code_to_name(code: str):
    from bs4 import BeautifulSoup

    params = {"code": code}
    response = requests.get(BASE_URL, params)
    soup = BeautifulSoup(response.text, "html.parser")
    name = soup.select_one(".h_company > .wrap_company > h2")

    return name.text
