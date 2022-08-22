import unittest

from naver_finance.synchronous.symbol_service import SyncSymbolService


class TestSyncCodeManager(unittest.TestCase):
    def setUp(self) -> None:
        self.service = SyncSymbolService()

    def tearDown(self) -> None:
        self.service.close()

    def test_code_to_name(self):
        # given
        code = "005930"
        # when
        name = self.service.code_to_name(code)
        # then
        self.assertEqual("삼성전자", name)

    def test_code_to_name_by_wrong_code_then_raise_AttributeError(self):
        wrong_code = "000000"
        with self.assertRaises(AttributeError):
            self.service.code_to_name(wrong_code)

    def test_name_to_code_list(self):
        # given
        name = "삼성"
        # when
        stocks = self.service.name_to_code_list(name)
        stocks = [*map(lambda s: s["code"], stocks)]
        # then
        self.assertTrue("005930" in stocks)

    def test_name_to_code_list_by_exactly_name(self):
        # given
        name = "삼성전자우"
        # when
        stocks = self.service.name_to_code_list(name)
        codes = [*map(lambda s: s["code"], stocks)]
        # then
        self.assertTrue("005935" in codes)

    def test_name_to_code_list_by_wrong_name_then_raise_AttributeError(self):
        name = "김지호"
        with self.assertRaises(AttributeError):
            self.service.name_to_code_list(name)

    def test_get_current_price_by_code(self):
        # given
        code = "000660"
        # when
        price = self.service.get_current_price_by_code(code)
        # then
        self.assertTrue(price != 0)

    def test_get_current_price_by_wrong_code_then_raise_AttributeError(self):
        with self.assertRaises(AttributeError):
            self.service.get_current_price_by_code("000000")
