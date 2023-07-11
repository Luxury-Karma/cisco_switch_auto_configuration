from Modules import Router
from Modules import Switch
from Modules import General_Machine
import sys
import os

__MAXIMUM_ATTEMPT: int = 5


def ensure_number(input_value: str) -> int or bool:
    try:
        number = int(input_value)  # Convert the input to a float number
        return number
    except ValueError:
        number = False
        return number


def ensure_ip(ip_a: str) -> [bool, str] or [bool, None]:
    j = 0
    while not General_Machine.validate_ip(ip_a) and j < __MAXIMUM_ATTEMPT:
        ip_a = input('Enter a correct IP and subnet in this format 0.0.0.0 0.0.0.0: ')
        j = j + 1
        if j >= 5:
            print('Too many attempts. Skipping this part.')
    if j < __MAXIMUM_ATTEMPT:
        return True, ip_a
    return False, None


def ensure_specific_ip(ip: str) -> [bool, str] or [bool, None]:
    j = 0
    ip_a = ip
    while not General_Machine.validate_pure_ip(ip) and j < __MAXIMUM_ATTEMPT:
        ip_a = input('Enter a correct IP in this format 0.0.0.0: ')
        j = j + 1
        if j >= __MAXIMUM_ATTEMPT:
            print('Too many attempts.')
    if j < __MAXIMUM_ATTEMPT:
        return True, ip_a
    return False, None


def dhcp() -> str | None:
    dhcp_pool_name = input('Enter the name of the pool: ')
    ip_address = input('Enter the IP and network of the pool: ')

    en = ensure_ip(ip_address)
    if en[0]:
        return Router.set_DHCP(dhcp_pool_name, en[1])
    else:
        print('Too many wrong IP addresses. Skipping this part.')


def vlan_dhcp() -> str:
    dhcp_pool_name = input('Name of the DHCP pool: ')
    ip_address = input('What is the IP and subnet for the DHCP: ')
    en = ensure_ip(ip_address)
    if en[0]:
        ip_address = en[1]
        all_cmd.extend(Router.set_DHCP(dhcp_pool_name, ip_address))
        interface_to_apply = input('Which interface is the VLAN linked to: ')
        return Router.set_VLAN_DHCP_IPv4(dhcp_pool_name, ip_address, interface_to_apply)
    else:
        print('Too many wrong IP addresses. Skipping this part.')


def saving() -> None:
    file_name = input("Enter the name of the file: ")
    script_path = os.path.abspath(__file__)
    directory_path = os.path.dirname(script_path)
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'w') as file:
        for elem in all_cmd:
            file.write(f'{elem}\n')
    print(f'Saved at path: {file_path}')


def static_trunking() -> str or None:
    port_to_trunk = input('Enter the port to trunk: ')
    vlan_to_allow = input('Enter the VLAN number\n (leave empty if all) (split the VLANs numbers with space): ')
    if vlan_to_allow and vlan_to_allow != '':
        vlan_to_allow = vlan_to_allow.split()
        return Switch.set_static_trunking(port_to_trunk, vlan_to_allow)
    else:
        return Switch.set_static_trunking(port_to_trunk, None)


def dot_dhcp() -> str | None:
    inter = input('Interface that has the multiple VLANs: ')
    vlan_number = input('What is the VLAN that needs to be applied: ')
    ip_address = input('What is the IP and subnet for the DHCP: ')
    en = ensure_ip(ip_address)
    if en[0]:
        ip_address = en[1]
        singular_ip = input('What is the IP of the gateway: ')
        if ensure_specific_ip(singular_ip):
            return Router.set_dot1q_ports_and_dhcp(inter, vlan_number, ip_address, singular_ip)
        else:
            print('Not an IP. Skipping this part.\n')
    else:
        print('Too many wrong IP addresses. Skipping this part.\n')


def house_keeping() -> str | None:
    machine_name = input('Enter the name of the machine: ')
    banner_message = input('Enter the banner: ')
    user = input('Enter the user: ')
    password = input('Enter the password of the user: ')
    secret = input('Enter the secret for the machine: ')
    return General_Machine.house_keeping(machine_name, banner_message, user, password, secret)


def dotq() -> str | None:
    inter = input('Enter the interface we are working with: ')
    dot = input('Enter all of the dotq ports (put a space in between each port '
                '(port needs to have the same number as VLAN)): ')
    dot = dot.split()
    dotl = []
    for elem in dot:
        singular_ip = input(f'What is the IP address for {elem}: ')
        if ensure_specific_ip(singular_ip):
            dotl.append([elem, singular_ip])
        else:
            print('Skipping this dot due to too many attempts.\n')
            pass
    return Router.set_dot1q_ports(inter, dotl)


def static_route() -> str | None:
    print('Input "quit" when you are done entering routes.')
    cont_route = True
    route = []
    while cont_route:
        ip_address = input('Enter the IP and subnet (split with space): ')
        if 'quit' in ip_address.lower().split():
            cont_route = False
        else:
            en = ensure_ip(ip_address)
            if en[0]:
                ip_address = en[1]
                route.append(ip_address.split())
            else:
                print('Wrong IP. Skipping this one.')
                pass
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
          '-ospf: create OSPF routes\n')


def ospf() -> str:
    p_id: str = input('Process ID: ')
    r_id: str = input('Router ID: ')
    area: str = input('Area: ')
    wildcard_mask: str = input('Wildcard mask (leave empty for default): ')
    wildcard_mask = wildcard_mask if wildcard_mask != '' else None
    final_road: bool = False
    total_road: list[str] = []
    while not final_road:
        n_road = ensure_ip(input('Enter "end" when over.\nEnter the new road IP: '))[1]

        if n_road and 'end' not in n_road:
            total_road.extend(n_road)
        elif n_road in n_road:
            final_road = True
        else:
            print('Not an IP. Continue.\n')
    return Router.set_ospf(p_id, r_id, total_road, area, wildcard_mask)


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
                input('Enter the port to dynamically desirable trunk: ')))

        if '-dta' in sys.argv:
            all_cmd.extend(Switch.set_dynamic_trunking_auto(input('Enter the port to dynamically auto trunk: ')))

        if '-dhcp' in sys.argv:
            all_cmd.extend(dhcp())

        if '-mdhcp' in sys.argv:
            number_of_pool = ensure_number(input('Number of pools: '))
            i = 0
            while not number_of_pool:
                number_of_pool = ensure_number(input('Enter a number of pools: '))
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
            amount_of_DHCP = ensure_number(input('How many VLAN DHCP need to be created: '))
            i = 0
            while not amount_of_DHCP:
                amount_of_DHCP = ensure_number(input('How many VLAN DHCP need to be created. IT NEEDS TO BE A NUMBER: '))
                i = i + 1
                if i >= 5:
                    print('Program quit, too many bad attempts: ')
            for e in range(amount_of_DHCP):
                vlan_dhcp()

        if '-dpdhcp' in sys.argv:
            all_cmd.extend(dot_dhcp())

        if '-mdphcp' in sys.argv:
            pools_amount = ensure_number(input('How many VLAN dotq ports need to be created: '))
            i = 0
            while not pools_amount:
                pools_amount = ensure_number(input('How many VLAN dotq need to be created. IT NEEDS TO BE A NUMBER: '))
                i = i + 1
                if i >= 5:
                    print("Program quit, too many bad attempts")
            interface = input('Which interface will receive the dotq ports: ')
            for e in range(pools_amount):
                all_cmd.extend(dot_dhcp())

        if '-dot' in sys.argv:
            all_cmd.extend(dotq())

        if '-str' in sys.argv:
            static_route()
        if '-ospf' in sys.argv:
            ospf()

        saving()
