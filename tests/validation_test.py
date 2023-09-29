import unittest
from utilities.validation import InputValidation

class TestValidation(unittest.TestCase):
    def test_valid_password(self):
        self.assertTrue(InputValidation.is_valid_password("'ASDdfg123!'#"))

    def test_scandinavian_character_is_special(self):
        self.assertTrue(InputValidation.is_valid_password("V4lidPässwörd"))

    def test_too_short_password(self):
        self.assertFalse(InputValidation.is_valid_password("$h0rtPW"))

    def test_too_long_password(self):
        password = "longl0nglonglonglonglonglonglongLONGlonglonglonglonglonglonglonglonglong!"
        self.assertFalse(InputValidation.is_valid_password(password))

    def test_no_special_character(self):
        self.assertFalse(InputValidation.is_valid_password("AlmostG00dPassword"))

    def test_no_digit(self):
        self.assertFalse(InputValidation.is_valid_password("AlmostGoodP@$$word!"))

    def test_no_capital_letter(self):
        self.assertFalse(InputValidation.is_valid_password("almostg00dpa$$word!"))

    def test_no_lower_case_character(self):
        self.assertFalse(InputValidation.is_valid_password("ALMOSTG00DPA$$WORD!"))
