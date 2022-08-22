from abc import ABCMeta, abstractmethod

from naver_finance.interfaces.common.service import Service


class Scraper(metaclass=ABCMeta):
    @abstractmethod
    def get_service(self) -> Service:
        pass
