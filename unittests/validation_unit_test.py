import unittest
import sys
sys.path.append("..")
from validation import is_valid_phone_number,is_valid_email


class TestStringMethods(unittest.TestCase):            
	def test_phone_number_validation(self):
		test_phone_numbers_1 = "+1 (555) 123-4567"
		test_phone_numbers_2 = "555-123-4567"
		test_phone_numbers_3 = "555 123 4567"
		test_phone_numbers_4 = "+44 (0) 20 1234 5678"
		test_phone_numbers_5 = "02012345678"
		test_phone_number_6 = "021helloworld3456"

		self.assertTrue(is_valid_phone_number(test_phone_numbers_1))
		self.assertTrue(is_valid_phone_number(test_phone_numbers_2))
		self.assertTrue(is_valid_phone_number(test_phone_numbers_3))
		self.assertTrue(is_valid_phone_number(test_phone_numbers_4))
		self.assertTrue(is_valid_phone_number(test_phone_numbers_5))
		self.assertFalse(is_valid_phone_number(test_phone_number_6))
	
	def test_email_is_valiad(self):
		email_address_without_delimeter = "helloworld.gmail.com"
		email_address_without_dotcom = "helloworld@."
		email_address_without_address = "@gmail.com"
		valid_email = "helloworld@gmail.com"
		self.assertFalse(is_valid_email(email_address_without_delimeter))
		self.assertFalse(is_valid_email(email_address_without_dotcom))
		self.assertFalse(is_valid_email(email_address_without_address))
		self.assertTrue(is_valid_email(valid_email))


if __name__ == '__main__':
    unittest.main()