from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from naver_finance.models import Symbol


class SymbolService(metaclass=ABCMeta):
    @abstractmethod
    def code_to_name(self, code: str) -> str:
        """종목코드를 받아 종목명을 반환합니다."""

    @abstractmethod
    def name_to_code_list(self, name: str) -> List["Symbol"]:
        """종목명을 받아 검색 결과를 매핑해서 종목 리스트를 반환합니다."""

    @abstractmethod
    def get_current_price_by_code(self, code: str) -> Union[int, float]:
        """종목코드를 받아 최근 체결가를 반환합니다.

        장이 열렸을 때 실시간 가격임을 보장하지 않습니다.
        """
