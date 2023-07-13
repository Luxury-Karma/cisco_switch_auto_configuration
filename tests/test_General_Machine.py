import unittest
from Modules.General_Machine import *

class HouseKeepingTestCase(unittest.TestCase):

    def test_house_keeping(self):
        machine_name = "Machine1"
        banner_message = "Welcome to Machine1"
        username = "admin"
        password = "password"
        secret = "mysecret"

        expected_result = [
            "enable secret mysecret",
            "hostname Machine1",
            "banner Welcome to Machine1",
            "username admin password password"
        ]

        result = house_keeping(machine_name, banner_message, username, password, secret)
        self.assertEqual(result, expected_result)

class ValidateIpTestCase(unittest.TestCase):
    def test_validate_ip(self):
        input_string_test_deux = '10.0.0.0 255.255.255.0'
        input_string_test_one = '10.0.0.0'
        input_string_test_trois = 'a'
        with_no_sub_net = False

        expected_restul_one = True
        expected_restul_deux = True
        expected_restul_trois = False
    pass

if __name__ == '__main__':
    unittest.main()
