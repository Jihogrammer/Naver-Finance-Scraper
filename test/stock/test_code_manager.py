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
