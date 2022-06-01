import unittest

from naver_finance.stock import code_manager


class TestCode(unittest.TestCase):
    def test_code_to_name(self):
        # given
        code = "005930"
        # when
        name = code_manager.code_to_name(code)
        # then
        self.assertEqual("삼성전자", name)

    def test_code_to_name_when_by_wrong_code_then_return_None(self):
        # given
        wrong_code = "000000"
        # when
        name = code_manager.code_to_name(wrong_code)
        # then
        self.assertEqual(None, name)

    def test_name_to_code_list(self):
        # given
        name = "삼성"
        # when
        stocks = code_manager.name_to_code_list(name)
        stocks = [*map(lambda s: s["code"], stocks)]
        # then
        self.assertTrue("005930" in stocks)

    def test_name_to_code_list_by_exactly_name(self):
        # given
        name = "삼성전자우"
        # when
        stocks = code_manager.name_to_code_list(name)
        codes = [*map(lambda s: s["code"], stocks)]
        # then
        self.assertTrue("005935" in codes)

    def test_name_to_code_list_when_by_wrong_name_then_return_empty_list(self):
        # given
        name = "김지호"
        # when
        stocks = code_manager.name_to_code_list(name)
        # then
        self.assertEqual([], stocks)

    def test_get_current_price_by_code(self):
        # given
        code = "000660"
        # when
        price = code_manager.get_current_price_by_code(code)
        # then
        self.assertTrue(price >= 1000)
