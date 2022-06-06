from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, List, Optional, Union

if TYPE_CHECKING:
    from naver_finance.models import Stock


class CodeManager(metaclass=ABCMeta):
    @abstractmethod
    def code_to_name(self, code: str) -> Optional[str]:
        pass

    @abstractmethod
    def name_to_code_list(self, name: str) -> List["Stock"]:
        pass

    @abstractmethod
    def get_current_price_by_code(self, code: str) -> Union[int, float]:
        pass
