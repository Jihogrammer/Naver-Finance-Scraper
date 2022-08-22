import unittest
import asyncio

from naver_finance.asynchronous.symbol_service import AsyncSymbolService


class TestAsyncCodeManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.service = AsyncSymbolService()

    def tearDown(self) -> None:
        asyncio.run(self.service.close())

    async def test_code_to_name(self):
        code = "005930"
        name = await self.service.code_to_name(code)
        self.assertEqual("삼성전자", name)

    async def test_code_to_name_by_wrong_code_then_raise_AttributeError(self):
        wrong_code = "000000"
        with self.assertRaises(AttributeError):
            await self.service.code_to_name(wrong_code)

    async def test_name_to_code_list(self):
        name = "삼성"
        stocks = await self.service.name_to_code_list(name)
        stocks = [*map(lambda s: s["code"], stocks)]
        self.assertTrue("005930" in stocks)

    async def test_name_to_code_list_by_exactly_name(self):
        name = "삼성전자우"
        stocks = await self.service.name_to_code_list(name)
        codes = [*map(lambda s: s["code"], stocks)]
        self.assertTrue("005935" in codes)

    async def test_name_to_code_list_by_wrong_name_raise_AttributeError(self):
        name = "jihogrammer"
        with self.assertRaises(AttributeError):
            await self.service.name_to_code_list(name)

    async def test_get_current_price_by_code(self):
        code = "000660"
        price = await self.service.get_current_price_by_code(code)
        self.assertTrue(price != 0)

    async def test_get_current_price_by_wrong_code_raise_AttributeError(self):
        with self.assertRaises(AttributeError):
            await self.service.get_current_price_by_code("000000")
