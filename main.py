"""
This script is used to automate the configuration of Cisco switches.
It provides functionality such as setting up DHCP, creating VLANs, setting up static routes, and more.
Usage: Run this script with the necessary flags to perform specific actions.
       Use '-h' flag to get a list of all available flags and their descriptions.

Author: Alexandre Gauvin
Date: 2023
Version: a0.0.1
"""

from Modules import Router
from Modules import Switch
from Modules import General_Machine
import sys
import os

from Modules.ErrorHandling import set_error, gld_errorlist, ASErr
import logging

# Set up logging
g_log = logging.getLogger('cisco_switch_auto_config')
g_hdlr = logging.FileHandler('cisco_switch_auto_config.log')
g_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
g_hdlr.setFormatter(g_formatter)
g_log.addHandler(g_hdlr)
g_log.setLevel(logging.INFO)
g_log.info('\n')
g_log.info('>>>>>>> Begin Process <<<<<<<')

try:
    __MAXIMUM_ATTEMPT: int = 5


    def typed_input(message: str, new_type: type = str) -> any:
        """
                Prompts user for input and checks if it matches the expected data type.
                If user enters 'end', the program ends.
                :param message: prompt message for the user
                :param new_type: expected data type of the input
                :return: user's input converted to the expected data type or None if conversion fails
                """
        res = None
        while not type(res) is new_type and not res == '':
            try:
                mes = input(message)
                if mes.strip().lower() == 'end':
                    set_error(n_code=1001,s_message='End was requested')
                    sys.exit(0)
                res = new_type(mes)
            except ValueError:
                print("wrong_data_type")
                res = None
        return res


    def tst_ip(with_subnet=True) -> [bool, str|None] :
        """
                Verifies that a user input is a valid IP address and, optionally, subnet.
                If the user fails to enter a valid IP/subnet after __MAXIMUM_ATTEMPT attempts, the function returns False.
                :param with_subnet: if True, expects the user to input both IP and subnet; otherwise, only IP is expected
                :return: [bool, str] if input is valid IP/subnet; [bool, None] if input is invalid after maximum attempts
                """
        message = '\tEnter a correct IP and subnet in this format 0.0.0.0 0.0.0.0: ' \
            if with_subnet else '\tEnter a correct IP in this format 0.0.0.0: '

        for i in range(0,__MAXIMUM_ATTEMPT):

            ip = typed_input(message)

            if ip.strip().lower() == 'quit':
                return True, 'quit'
            if General_Machine.validate_ip(ip, with_subnet=with_subnet):
                return True, ip

        print('Too many attempts.')
        return False, None
    def request_ip(message, with_subnet=True):
        print(message, '\n')

        #is_ip, ip = ensure_ip_subnet('') if with_sub_net else ensure_ip('')
        is_ip, ip = tst_ip(with_subnet=with_subnet)
        if is_ip:
            return ip
        else:
            set_error(n_code=-500, s_message='Ip went wrong')
            raise Exception


    def dhcp() -> str | None:
        dhcp_pool_name = typed_input('Enter the name of the pool: ')
        ip = request_ip('Enter the IP and network of the pool:')
        return Router.set_DHCP(dhcp_pool_name, ip)


    def hsrp() -> str or None:
        print('Enter HSRP')
        internal_interface = typed_input('What is the internal interface: ')
        internal_virtual_ip = request_ip('What is the internal virtual IP: ', False)

        internal_hsrp_process = typed_input('What is the internal virtual hsrp: ')

        external_interface = typed_input('What is the external interface: ')
        external_virtual_ip = request_ip('What is the virtual external IP: ', False)

        external_hsrp_process = typed_input('What is the virtual external hsrp: ')
        all_cmd.extend(Router.configure_hsrp(internal_interface, internal_virtual_ip, internal_hsrp_process,
                                             external_interface, external_virtual_ip, external_hsrp_process))
        return None


    def vlan_dhcp() -> str:
        dhcp_pool_name = typed_input('Name of the DHCP pool: ')
        ip_address = request_ip('What is the IP and subnet for the DHCP: ')
        all_cmd.extend(Router.set_DHCP(dhcp_pool_name, ip_address))
        interface_to_apply = typed_input('Which interface is the VLAN linked to: ')
        return Router.set_VLAN_DHCP_IPv4(dhcp_pool_name, ip_address, interface_to_apply)


    def saving() -> None:
        file_name = typed_input("Enter the name of the file: ")
        script_path = os.path.abspath(__file__)
        directory_path = os.path.dirname(script_path)
        file_path = os.path.join(directory_path, f'{file_name}.txt')
        with open(file_path, 'w') as file:
            for elem in all_cmd:
                file.write(f'{elem}\n')
        print(f'Saved at path: {file_path}')


    def static_trunking() -> str or None:
        port_to_trunk = typed_input('Enter the port to trunk: ')
        vlan_to_allow = typed_input(
            'Enter the VLAN number\n (leave empty if all) (split the VLANs numbers with space): ')
        if vlan_to_allow and vlan_to_allow != '':
            vlan_to_allow = vlan_to_allow.split()
            return Switch.set_static_trunking(port_to_trunk, vlan_to_allow)
        else:
            return Switch.set_static_trunking(port_to_trunk, None)


    def dot_dhcp() -> str | None:
        inter = typed_input('Interface that has the multiple VLANs: ')
        vlan_number = typed_input('What is the VLAN that needs to be applied: ')
        ip_address = request_ip('What is the IP and subnet for the DHCP: ')
        singular_ip = request_ip('What is the IP of the gateway: ')
        return Router.set_dot1q_ports_and_dhcp(inter, vlan_number, ip_address, singular_ip)


    def house_keeping() -> str | None:
        machine_name = typed_input('Enter the name of the machine: ')
        banner_message = typed_input('Enter the banner: ')
        user = typed_input('Enter the user: ')
        password = typed_input('Enter the password of the user: ')
        secret = typed_input('Enter the secret for the machine: ')
        return General_Machine.house_keeping(machine_name, banner_message, user, password, secret)


    def dotq() -> str | None:
        inter = typed_input('Enter the interface we are working with: ')
        dot = typed_input('Enter all of the dotq ports (put a space in between each port '
                          '(port needs to have the same number as VLAN)): ')
        dot = dot.split()
        dotl = []
        for elem in dot:
            singular_ip = request_ip(f'What is the IP address for {elem}: ', False)
            dotl.append([elem, singular_ip])
        return Router.set_dot1q_ports(inter, dotl)


    def static_route() -> str | None:
        print('Input "quit" when you are done entering routes.')
        cont_route = True
        route = []
        while cont_route:
            ip_address = request_ip('Enter the IP and subnet (split with space): ')
            if 'quit' in ip_address.lower():
                cont_route = False
            else:
                route.append(ip_address.split())
        return Router.static_routing(route)


    def helper() -> None:
        """
        Give all the functions command
        :return: Nothing
        """
        print('-k: housekeeping\n'
              '-st: create a static trunk port\n'
              '-dtd: create a dynamic desirable trunk\n'
              '-dta: create a dynamic auto trunk\n'
              '-dhcp: create a DHCP in the router\n'
              '-vdhcp: create a DHCP for the VLAN\n'
              '-mvdhcp: create multiple DHCP for VLANs\n'
              '-dpdhcp: create a dot1q port and a DHCP with it\n'
              '-mdphcp: create multiple dot1q ports and a DHCP with each one\n'
              '-dot: create a dotq on an interface\n'
              '-str: create static routes\n'
              '-ospf: create OSPF routes\n'
              '-acl: activate ACL\n'
              '-nato: activate NAT Overload\n')


    def ospf() -> str:
        p_id: str = typed_input('Process ID: ', int)
        r_id: str = request_ip('Router ID: ', False)
        area: str = typed_input('Area: ', int)
        final_road: bool = False
        total_road: list[str] = []
        while not final_road:
            n_road = request_ip('Enter "quit" when over.\n\tEnter the new road IP and wildcard: ')
            if 'quit' != n_road:
                if n_road:
                    total_road.append(n_road)
                else:
                    print('Not an IP. Continue.\n')
            if 'quit' == n_road:
                final_road = True
                pass
        return Router.set_ospf(p_id, r_id, total_road, area)


    def nat_overload() -> str or None:
        inter = typed_input('What is the internal interface: ')
        network = request_ip('What is the IP and the subnet of inner network: ')
        ex_inter = typed_input('Whant is the external interface: ')
        ex_network = request_ip('What is the public ip and subnet: ')

        for i in range(0, __MAXIMUM_ATTEMPT):
            acl_number = typed_input('Enter ACL number', int)

            if acl_number < 1 or (99 < acl_number < 1000) or acl_number > 2699:
                set_error(n_code=-501, s_description='Invalid access list number. Please enter a number between 1 and'
                                                     ' 99 or between 1000 and 2699.')
                continue
            return Router.generate_nat_overload_config(inter, network[1], ex_inter, ex_network[1], acl_number)


    def verify_its_number(user_input: str) -> int or None:
        j = 0
        while not user_input.isdigit() and j < __MAXIMUM_ATTEMPT:
            print('Invalid access list number. Please enter a numeric value.')
            user_input = typed_input('Enter the access list number')
            j = j + 1
            if j >= __MAXIMUM_ATTEMPT:
                print('To many bad attempt skiping access list')
        return int(user_input) if user_input.isdigit() else None


    def access_list() -> str or None:
        ac_l_number = typed_input('Enter the access list number', int)

        for i in range(0, __MAXIMUM_ATTEMPT):
            acl_number = typed_input('Enter ACL number', int)

            if acl_number < 1 or (99 < acl_number < 1000) or acl_number > 2699:
                set_error(n_code=-501, s_description='Invalid access list number. Please enter a number between 1 and'
                                                     ' 99 or between 1000 and 2699.')
                continue

            permit_or_deny = typed_input('If the permit is true please enter "TRUE" else enter anything (AKA. FALSE)')
            if permit_or_deny.strip().lower() == 'true':
                permit_or_deny = True
            else:
                permit_or_deny = False
            source_ip = request_ip('Enter the source IP for ACL (ip mask): ')
            return Router.create_access_list(ac_l_number, permit_or_deny, source_ip[1])

        return None


    if __name__ == '__main__':
        if len(sys.argv) > 1:
            all_cmd = []
            if '-h' in sys.argv:
                helper()
            else:
                if '-k' in sys.argv:
                    all_cmd.extend(house_keeping())

                if '-st' in sys.argv:
                    all_cmd.extend(static_trunking())

                if '-dtd' in sys.argv:
                    all_cmd.extend(Switch.set_dynamic_trunking_desirable(
                        typed_input('Enter the port to dynamically desirable trunk: ')))

                if '-dta' in sys.argv:
                    all_cmd.extend(
                        Switch.set_dynamic_trunking_auto(typed_input('Enter the port to dynamically auto trunk: ')))

                if '-dhcp' in sys.argv:
                    all_cmd.extend(dhcp())

                if '-mdhcp' in sys.argv:
                    number_of_pool = typed_input('Number of pools: ', int)
                    i = 0
                    while not number_of_pool:
                        number_of_pool = typed_input('Enter a number of pools: ', int)
                        i = i + 1
                        if i >= 5:
                            print('ERROR WITH NUMBER, TOO MANY BAD ATTEMPTS\n')
                            number_of_pool = 0
                            break

                    for e in range(number_of_pool):
                        all_cmd.extend(dhcp())

                if '-vdhcp' in sys.argv:
                    vlan_dhcp()

                if '-mvdhcp' in sys.argv:
                    amount_of_DHCP = typed_input('How many VLAN DHCP need to be created: ', int)
                    i = 0
                    while not amount_of_DHCP:
                        amount_of_DHCP = typed_input('How many VLAN DHCP need to be created. IT NEEDS TO BE A NUMBER: ',
                                                     int)
                        i = i + 1
                        if i >= 5:
                            print('Program quit, too many bad attempts: ')
                    for e in range(amount_of_DHCP):
                        vlan_dhcp()

                if '-dpdhcp' in sys.argv:
                    all_cmd.extend(dot_dhcp())

                if '-mdphcp' in sys.argv:
                    pools_amount = typed_input('How many VLAN dotq ports need to be created: ', int)
                    i = 0
                    while not pools_amount:
                        pools_amount = typed_input('How many VLAN dotq need to be created. IT NEEDS TO BE A NUMBER: ', int)
                        i = i + 1
                        if i >= 5:
                            print("Program quit, too many bad attempts")
                    interface = typed_input('Which interface will receive the dotq ports: ')
                    for e in range(pools_amount):
                        all_cmd.extend(dot_dhcp())

                if '-dot' in sys.argv:
                    all_cmd.extend(dotq())

                if '-str' in sys.argv:
                    all_cmd.extend(static_route())
                if '-ospf' in sys.argv:
                    all_cmd.extend(ospf())

                if '-acl' in sys.argv:
                    all_cmd.extend(access_list())

                if '-nato' in sys.argv:
                    all_cmd.extend(nat_overload())

                saving()

except ASErr:
    print(gld_errorlist)
except:
    set_error()
    print(gld_errorlist)
finally:
    g_log.info('\n')
    g_log.info(str(gld_errorlist))
    g_log.info('>>>>>>> Process End <<<<<<<')
