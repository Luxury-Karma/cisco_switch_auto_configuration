import unittest
from unittest.mock import patch
from io import StringIO
from main import *


class TestScript(unittest.TestCase):

    @patch('builtins.input', side_effect=['Test Name'])
    def test_typed_input(self, mock_input):
        res = typed_input('Enter a message: ', str)
        self.assertEqual(res, 'Test Name')

    @patch('builtins.input', side_effect=['192.168.0.1'])
    def test_tst_ip(self, mock_input):
        res = tst_ip(with_subnet=True)
        self.assertEqual(res, (True, '192.168.0.1'))

    @patch('builtins.input', side_effect=['192.168.0.1'])
    def test_request_ip(self, mock_input):
        res = request_ip('Enter a message: ', with_subnet=True)
        self.assertEqual(res, '192.168.0.1')

    def test_dhcp(self):
        res = dhcp()
        self.assertEqual(res, 'DHCP Configuration Command')

    @patch('builtins.input', side_effect=['Internal Interface', '192.168.0.2', 'HSRP Process',
                                          'External Interface', '192.168.0.3', 'HSRP Process'])
    def test_hsrp(self, mock_input):
        all_cmd = []
        hsrp(all_cmd)
        self.assertEqual(all_cmd, ['HSRP Configuration Command 1', 'HSRP Configuration Command 2'])

    def test_vlan_dhcp(self):
        res = vlan_dhcp()
        self.assertEqual(res, 'VLAN DHCP Configuration Command')

    def test_saving(self):
        all_cmd = ['Command 1', 'Command 2', 'Command 3']
        saving(all_cmd)
        # Assert that the commands are saved to the file as expected

    @patch('builtins.input', side_effect=['Port to Trunk', '1 2 3'])
    def test_static_trunking(self, mock_input):
        res = static_trunking()
        self.assertEqual(res, 'Static Trunking Configuration Command')

    @patch('builtins.input', side_effect=['Interface', 'VLAN Number', 'IP Address', 'Gateway IP'])
    def test_dot_dhcp(self, mock_input):
        res = dot_dhcp()
        self.assertEqual(res, 'Dot1q Ports and DHCP Configuration Command')

    @patch('builtins.input', side_effect=['Machine Name', 'Banner Message', 'User', 'Password', 'Secret'])
    def test_house_keeping(self, mock_input):
        res = house_keeping()
        self.assertEqual(res, 'Housekeeping Configuration Commands')

    @patch('builtins.input', side_effect=['Interface', '1 2 3', 'IP Address'])
    def test_dotq(self, mock_input):
        res = dotq()
        self.assertEqual(res, 'Dotq Configuration Command')

    @patch('builtins.input', side_effect=[True, '192.168.0.1 255.255.255.0'])
    def test_static_route(self, mock_input):
        res = static_route()
        self.assertEqual(res, 'Static Route Configuration Command')

    def test_helper(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        helper()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        self.assertEqual(output, '-k: housekeeping\n-st: create a static trunk port\n-dtd: create a dynamic desirable trunk\n-dta: create a dynamic auto trunk\n-dhcp: create a DHCP in the router\n-vdhcp: create a DHCP for the VLAN\n-mvdhcp: create multiple DHCP for VLANs\n-dpdhcp: create a dot1q port and a DHCP with it\n-mdphcp: create multiple dot1q ports and a DHCP with each one\n-dot: create a dotq on an interface\n-str: create static routes\n-ospf: create OSPF routes\n-acl: activate ACL\n-nato: activate NAT Overload\n-v : set vlan')

    @patch('builtins.input', side_effect=['Process ID', 'Router ID', 'Area', '192.168.0.1 0.0.0.255', 'quit'])
    def test_ospf(self, mock_input):
        res = ospf()
        self.assertEqual(res, 'OSPF Configuration Commands')

    def test_set_vlan(self):
        res = set_vlan()
        self.assertEqual(res, ['VLAN Configuration Command 1', 'VLAN Configuration Command 2'])

    @patch('builtins.input', side_effect=['Internal Interface', '192.168.0.1', 'External Interface', '192.168.0.2'])
    def test_nat_overload(self, mock_input):
        res = nat_overload()
        self.assertEqual(res, 'NAT Overload Configuration Command')

    @patch('builtins.input', side_effect=['Access List Number', 'ACL Number', 'true', '192.168.0.1 255.255.255.0'])
    def test_access_list(self, mock_input):
        res = access_list()
        self.assertEqual(res, 'Access List Configuration Command')

if __name__ == '__main__':
    unittest.main()
