from abc import ABCMeta, abstractmethod

from bs4 import BeautifulSoup


class Service(metaclass=ABCMeta):
    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def _fetch(self, url: str) -> str:
        pass

    def make_soup(self, html: str) -> "BeautifulSoup":
        return BeautifulSoup(html, "html.parser")
