"""
The goal of this project is to make that with a simple script we can get the output to all switches and router settings
"""







# todo: all the methode to setup any network machine
class General_Network_Machine():
    def house_keeping(self, machine_name: str, banner_message: str, username: str, password: str, secret: str):
        return [f'enable secret {secret}', f'hostname {machine_name}', f'banner {banner_message}',
                f'username {username} password {password}', ]


# todo: all the methode to setup a switch
class Switch(General_Network_Machine):

    def __init__(self):
        super().__init__()

    def set_vlan(self, vlan_name: str, vlan_number: str, vlan_ip: str):
        """
        Set up a vlan
        :param vlan_name: The name of the vlan if empty one is generated
        :param vlan_number: witch vlan we want to create
        :param vlan_ip: what will be the ip and subnet of the vlan. if you want dhcp you can write dhcp
        :return: the command to accomplish a perfect vlan
        """
        vlan_name = vlan_name if vlan_name else f'vlan{vlan_number}'
        return [f'vlan {vlan_number}', f'name {vlan_name}', f'interface vlan {vlan_number}', f'ip address {vlan_ip}',
                'no shutdown']

    def set_port_vlan(self, interface: str, vlan_number: str):
        """
        Set the vlan for the interface
        :param interface: wich interface is to setup
        :param vlan_number: wich vlan is suppose to handle it
        :return: the command to give a vlan to a interface
        """
        return[f'interface {interface}', f'switchport access vlan {vlan_number}']

    def set_static_trunking(self, port_to_trunk: str, vlan_to_allow: str):
        """
        Make a static trunk in the vlan
        :param port_to_trunk: witch interface we need to make a trunk
        :param vlan_to_allow: wich vlan are allowed (if empty all)
        :return:
        """
        vlan_to_allow = vlan_to_allow if vlan_to_allow else 'all'
        return [f'interface {port_to_trunk}', f'switchport mode trunk', f'switchport trunk allowed vlan {vlan_to_allow}']

    def set_dynamic_trunking_desirable(self, port_to_trunk: str):
        """
        Create a dynamic desirable trunk.
        :param port_to_trunk: Wich port will be the desirable trunk
        :return: the command to do it
        """
        return [f'interface {port_to_trunk}', 'switchport mode dynamic desirable']

    def set_dynamic_trunking_auto(self, port_to_trunk: str):
        """
        Create a dynamic auto trunk
        :param port_to_trunk: wich port to trunk
        :return: the command to do it
        """
        return [f'interface {port_to_trunk}', 'switchport mode dynamic auto']



# todo : all the methode to setup a switch
class Router(General_Network_Machine):

    def __init__(self):
        super().__init__()

    def set_DHCP(self, dhcp_pool_name: str, ip_address_and_subnet: str):
        return [f'end', f'configure terminal', f'ip dhcp pool {dhcp_pool_name}', f'network {ip_address_and_subnet}']

    def set_VLAN_DHCP_IPv4(self, dhcp_pool_name: str, ip_address_and_subnet: str, interface_to_apply: str):
        commands = self.set_DHCP(dhcp_pool_name, ip_address_and_subnet)
        commands.extend([f'interface {interface_to_apply}',
                         f'ip address {ip_address_and_subnet}',
                         f'ip address dhcp server {dhcp_pool_name}',
                         'no shutdown', 'exit'])
        return commands

    def set_VLAN_DHCP_IPv6(self, dhcp_pool_name: str, ipv6_address_and_prefix: str, interface_to_apply: str):
        return [f'end', f'configure terminal', f'ipv6 dhcp pool {dhcp_pool_name}',
                    f'address prefix {ipv6_address_and_prefix}',f'interface {interface_to_apply}',
                         f'ipv6 address {ipv6_address_and_prefix}',
                         f'ipv6 dhcp server {dhcp_pool_name}',
                         'no shutdown', 'exit']

    def set_OSPF_on_router(self, process_id: str, router_id: str, all_route: list[str], area: str, wildcard_mask: str):
        wildcard_mask = wildcard_mask if wildcard_mask else '0.0.0.0'
        base_command = ['end', 'configure terminal', f'router ospf {process_id}', f'router-id {router_id}']
        for e in all_route:
            base_command.append(f'network {e} {wildcard_mask} area {area}')
        base_command.append('exit')
        return base_command


    def set_OSPF_on_router_IPV6(self, process_id: str, router_id: str, all_route: list[str], area: str):
        base_command = ['end', 'configure terminal', f'ipv6 router ospf {process_id}', f'router-id {router_id}']
        for e in all_route:
            base_command.extend(['interface {}'.format(e), f'ipv6 ospf {process_id} area {area}'])
        base_command.append('exit')
        return base_command

    def static_routing(self, ip_route: list[list[str]]):
        base_command = ['end', 'configure terminal']
        for e in ip_route:
            base_command.append(f'ip route {e[0]} {e[1]}')
        base_command.append('exit')
        return base_command

    def set_dot1q_ports(self, interface: str, interface_dot: list[list[str]]):
        commands = [f'interface {interface}', 'no shutdown']
        for el in interface_dot:
            commands.extend(
                [f'interface {interface}.{el[0]}', f'encapsulation dot1Q {el[0]}', f'ip address {el[1].split()[0]}',
                 'no shutdown'])
        return commands

    # TODO: need correction of all the command
    def set_dot1q_ports_and_dhcp_IPV6(self, interface: str, vlan_number: str, ipv6_address: str, prefix_length: str):
        command =[f'interface {interface}', 'no shutdown']
        command.extend(self.set_VLAN_DHCP_IPv6(f'vlan{vlan_number}', f'{ipv6_address}/{prefix_length}',interface))
        command.extend([
            f'interface {interface}',
            'no shutdown',
            '!',
            f'interface {interface}.{vlan_number}',
            f'encapsulation dot1Q {vlan_number}',
            f'ipv6 address {ipv6_address}/{prefix_length}',
            'no shutdown',
            '!',
            f'ipv6 dhcp pool VLAN{vlan_number}',
            f'address prefix {ipv6_address}/{prefix_length}',
            f'default-router {ipv6_address}',
        ])
        return command

    def set_dot1q_ports_and_dhcp(self, interface: str, vlan_number, ip, subnet):
        command = [
            f'interface {interface}',
            f'no shutdown',
            '!',
            f'interface {interface}.{vlan_number}',
            f'encapsulation dot1Q {vlan_number}',
            f'ip address {ip} {subnet}',
            f'no shutdown',
            '!',
            f'ip dhcp pool VLAN{vlan_number}',
            f'network {ip} {subnet}',
            f'default-router {ip}',
            f'option 150 ip {ip}'
        ]
        return command

print('S1\n')
testS = Switch()
all_cmd = []
all_cmd.extend(testS.house_keeping('S1', 'hello', 'student', 'cisco123', 'cisco'))
all_cmd.extend(testS.set_vlan(None, '11', '11.0.0.0 255.0.0.0'))  # Example IPv6 address and prefix
all_cmd.extend(testS.set_port_vlan('fa 1/1', '10'))
all_cmd.extend(testS.set_vlan(None, '12', '12.0.0.0 255.0.0.0'))
all_cmd.extend(testS.set_port_vlan('fa 2/1', '11'))
all_cmd.extend(testS.set_static_trunking('fa 0/1', None))
for e in all_cmd:
    print(e)

print('\nS2\n')
all_cmd = []
all_cmd.extend(testS.house_keeping('S2', 'hello', 'student', 'cisco123', 'cisco'))
all_cmd.extend(testS.set_vlan(None, '13', '13.0.0.0 255.0.0.0'))  # Example IPv6 address and prefix
all_cmd.extend(testS.set_port_vlan('fa 1/1', '13'))
all_cmd.extend(testS.set_vlan(None, '14', '14.0.0.0 255.0.0.0'))
all_cmd.extend(testS.set_port_vlan('fa 2/1', '14'))
all_cmd.extend(testS.set_static_trunking('fa 0/1', None))
for e in all_cmd:
    print(e)

print('\nR1\n')

testR = Router()
all_cmd = []
all_cmd.extend(testR.set_DHCP('11', '11.0.0.0 255.0.0.0'))
all_cmd.extend(testR.set_DHCP('12', '12.0.0.0 255.0.0.0'))
all_cmd.extend(testR.set_DHCP('13', '13.0.0.0 255.0.0.0'))
all_cmd.extend(testR.set_DHCP('14', '14.0.0.0 255.0.0.0'))
all_cmd.extend(testR.set_OSPF_on_router('1', '1.1.1.1', ['10.0.0.0'], '0', None))

for e in all_cmd:
    print(e)







