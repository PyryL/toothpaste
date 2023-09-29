import unittest
from utilities.validation import InputValidation

class TestValidation(unittest.TestCase):
    def test_valid_password(self):
        self.assertTrue(InputValidation.is_valid_password("'ASDdfg123!'#"))

    def test_password_scandinavian_character_is_special(self):
        self.assertTrue(InputValidation.is_valid_password("V4lidPässwörd"))

    def test_too_short_password(self):
        self.assertFalse(InputValidation.is_valid_password("$h0rtPW"))

    def test_too_long_password(self):
        password = "longl0nglonglonglonglonglonglongLONGlonglonglonglonglonglonglonglonglong!"
        self.assertFalse(InputValidation.is_valid_password(password))

    def test_password_no_special_character(self):
        self.assertFalse(InputValidation.is_valid_password("AlmostG00dPassword"))

    def test_password_no_digit(self):
        self.assertFalse(InputValidation.is_valid_password("AlmostGoodP@$$word!"))

    def test_password_no_capital_letter(self):
        self.assertFalse(InputValidation.is_valid_password("almostg00dpa$$word!"))

    def test_password_no_lower_case_character(self):
        self.assertFalse(InputValidation.is_valid_password("ALMOSTG00DPA$$WORD!"))


    def test_valid_username(self):
        self.assertTrue(InputValidation.is_valid_username("John_Doe04"))

    def test_valid_username_without_underscore(self):
        self.assertTrue(InputValidation.is_valid_username("JohnDoe04"))

    def test_valid_username_without_lower_case(self):
        self.assertTrue(InputValidation.is_valid_username("JOHN_DOE04"))

    def test_valid_username_without_upper_case(self):
        self.assertTrue(InputValidation.is_valid_username("john_doe04"))

    def test_valid_username_without_digits(self):
        self.assertTrue(InputValidation.is_valid_username("John_Doe"))

    def test_too_short_username(self):
        self.assertFalse(InputValidation.is_valid_username("Jd"))

    def test_too_long_username(self):
        self.assertFalse(InputValidation.is_valid_username("John_Doe_2004"))

    def test_special_character_in_username(self):
        self.assertFalse(InputValidation.is_valid_username("JohnDoe!"))
