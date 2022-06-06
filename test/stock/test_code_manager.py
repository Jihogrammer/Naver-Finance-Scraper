from abc import ABCMeta, abstractmethod
from argparse import ArgumentError
import unittest

from naver_finance.config.constants import BASE_URL
from httpx import AsyncClient, Client


class __CodeManagerTester(metaclass=ABCMeta):
    @abstractmethod
    def test_code_to_name(self):
        """종목코드를 종목명으로 제대로 변환하는지"""

    @abstractmethod
    def test_code_to_name_by_wrong_code_then_return_None(self):
        """잘못된 종목코드로 종목명을 요청했을 때 None을 리턴하는지"""

    @abstractmethod
    def test_name_to_code_list(self):
        """종목명으로 검색했을 때 종목들 검색결과"""

    @abstractmethod
    def test_name_to_code_list_by_exactly_name(self):
        """정확한 종목명으로 검색했을 때 해당 종목이 리스트에 담겨 있는지"""

    @abstractmethod
    def test_name_to_code_list_by_wrong_name_then_return_empty_list(self):
        """잘못된 종목명으로 검색한 결과 종목 리스트가 비어있는지"""

    @abstractmethod
    def test_get_current_price_by_code(self):
        """종목 코드를 통해 최근 체결가 조회"""

    @abstractmethod
    def test_get_current_price_by_wrong_code_then_throws_error(self):
        """잘못된 종목 코드를 통해 최근 체결가 조회 시 예외 발생하는지"""


class TestAsyncCodeManager(unittest.IsolatedAsyncioTestCase, __CodeManagerTester):
    def setUp(self) -> None:
        from naver_finance.code_manager.async_code_manager import code_manager

        code_manager._client = AsyncClient(base_url=BASE_URL)
        self.client = code_manager

    def tearDown(self) -> None:
        import asyncio

        asyncio.run(self.client.close())

    async def test_code_to_name(self):
        # given
        code = "005930"
        # when
        name = await self.client.code_to_name(code)
        # then
        self.assertEqual("삼성전자", name)

    async def test_code_to_name_by_wrong_code_then_return_None(self):
        # given
        wrong_code = "000000"
        # when
        name = await self.client.code_to_name(wrong_code)
        # then
        self.assertEqual(None, name)

    async def test_name_to_code_list(self):
        # given
        name = "삼성"
        # when
        stocks = await self.client.name_to_code_list(name)
        stocks = [*map(lambda s: s["code"], stocks)]
        # then
        self.assertTrue("005930" in stocks)

    async def test_name_to_code_list_by_exactly_name(self):
        # given
        name = "삼성전자우"
        # when
        stocks = await self.client.name_to_code_list(name)
        codes = [*map(lambda s: s["code"], stocks)]
        # then
        self.assertTrue("005935" in codes)

    async def test_name_to_code_list_by_wrong_name_then_return_empty_list(self):
        # given
        name = "김지호"
        # when
        stocks = await self.client.name_to_code_list(name)
        # then
        self.assertEqual([], stocks)

    async def test_get_current_price_by_code(self):
        # given
        code = "000660"
        # when
        price = await self.client.get_current_price_by_code(code)
        # then
        self.assertTrue(price != 0)

    async def test_get_current_price_by_wrong_code_then_throws_error(self):
        with self.assertRaises(ArgumentError):
            await self.client.get_current_price_by_code("000000")


class TestSyncCodeManager(unittest.TestCase, __CodeManagerTester):
    def setUp(self) -> None:
        from naver_finance.code_manager.code_manager import code_manager

        code_manager._client = Client(base_url=BASE_URL)
        self.client = code_manager

    def tearDown(self) -> None:
        self.client.close()

    def test_code_to_name(self):
        # given
        code = "005930"
        # when
        name = self.client.code_to_name(code)
        # then
        self.assertEqual("삼성전자", name)

    def test_code_to_name_by_wrong_code_then_return_None(self):
        # given
        wrong_code = "000000"
        # when
        name = self.client.code_to_name(wrong_code)
        # then
        self.assertEqual(None, name)

    def test_name_to_code_list(self):
        # given
        name = "삼성"
        # when
        stocks = self.client.name_to_code_list(name)
        stocks = [*map(lambda s: s["code"], stocks)]
        # then
        self.assertTrue("005930" in stocks)

    def test_name_to_code_list_by_exactly_name(self):
        # given
        name = "삼성전자우"
        # when
        stocks = self.client.name_to_code_list(name)
        codes = [*map(lambda s: s["code"], stocks)]
        # then
        self.assertTrue("005935" in codes)

    def test_name_to_code_list_by_wrong_name_then_return_empty_list(self):
        # given
        name = "김지호"
        # when
        stocks = self.client.name_to_code_list(name)
        # then
        self.assertEqual([], stocks)

    def test_get_current_price_by_code(self):
        # given
        code = "000660"
        # when
        price = self.client.get_current_price_by_code(code)
        # then
        self.assertTrue(price != 0)

    def test_get_current_price_by_wrong_code_then_throws_error(self):
        with self.assertRaises(ArgumentError):
            self.client.get_current_price_by_code("000000")
