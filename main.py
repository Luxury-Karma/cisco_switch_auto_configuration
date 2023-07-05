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

    def set_vlan_dhcp_ipv4(self, dhcp_pool_name: str, ip_address_and_subnet: str, interface_to_apply: str):
        """
        Set up DHCP for specific port for a vlan
        :param dhcp_pool_name: the name of the pool
        :param ip_address_and_subnet: the ip of the pool
        :param interface_to_apply: which interface
        :return: all the command
        """
        commands = self.set_DHCP(dhcp_pool_name, ip_address_and_subnet)
        commands.extend([f'interface {interface_to_apply}',
                         f'ip address {ip_address_and_subnet}',
                         f'ip address dhcp server {dhcp_pool_name}',
                         'no shutdown', 'exit'])
        return commands

    def set_vlan_dhcp_ipv6(self, dhcp_pool_name: str, ip_address_and_subnet: str, vlan_number: str,
                           interface_to_apply: str):
        """
        Set up DHCP for specific port for a vlan
        :param dhcp_pool_name: the name of the pool
        :param ip_address_and_subnet: the ip of the pool
        :param vlan_number: wich vlan
        :param interface_to_apply: wich interface
        :return: all the command
        """
        return ['end','configure terminal', f'ipv6 dhcp pool {dhcp_pool_name}', f'address prefix {ip_address_and_subnet}',
                f'interface {interface_to_apply}', f'encapsulation dot1Q {vlan_number}', f'ipv6 address {ip_address_and_subnet}',
                f'ipv6 dhcp server {dhcp_pool_name}', 'no shutdown', 'exit']

    def set_ospf_on_router(self, process_id:str, router_id: str, all_route: list[str], area: str):
        """
        Make a working OSFP
        :param process_id: wich process is doing the ospf
        :param router_id: what is the id of the router
        :param all_route: what are the routs possible
        :param area: wich area are they in
        :return: the commands
        """
        base_command = ['end', 'configure terminal', f'router ospf {process_id}', f'router-id {router_id}']
        for e in all_route:
            base_command.append(f'network {e} area {area}')
        return base_command.append('exit')

    def set_ospf_on_router_IPV6(self, process_id: str, router_id: str, all_route: list[str], area: str):
        """
        Make a working OSFP
        :param process_id: wich process is doing the ospf
        :param router_id: what is the id of the router
        :param all_route: what are the routs possible
        :param area: wich area are they in
        :return: the commands
        """
        base_command = ['end', 'configure terminal', f'ipv6 router ospf {process_id}', f'router-id {router_id}']
        for e in all_route:
            base_command.append(f'area {area} range {e}')
        return base_command.append('exit')

    def static_routing(self, ip_route: list[list[str]]):
        """
        Make static route for IPV4
        :param ip_route: An array with the network we want to go and the next hop
        :return: the command to accomplish it
        """
        base_command = ['end', 'configure terminal']
        for e in ip_route:
            base_command.append(f'ip route {e[0]} {e[1]}')
        base_command.append('exit')
        return base_command
    def set_dotq_ports(self, interface: str, interface_dot: list[list[str]]):
        """
        Set the dot1q for the ports
        :param interface: The interface where the dot1q is
        :param interface_dot: the data in this format: [[ 'vlan number', 'ip subnet']]
        :return: the commands
        """
        commands = [f'interface {interface}', 'no shutdown']
        for el in interface_dot:
            commands.extend(
                [f'interface {interface}.{el[0]}', f'encapsulation dot1Q {el[0]}', f'ip address {el[1].split()[0]}',
                 'no shutdown'])
        return commands

    def set_dotq_ports_and_dhcp(self, interface: str, vlan_number, ip, subnet):
        command =[
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
         f'option 150 ip {ip}']

        return command


print('S1 \n')
testS = Switch()
testR = Router()
all_cmd = []
all_cmd.extend(testS.house_keeping('S1', 'hello', 'student', 'cisco123', 'cisco'))
all_cmd.extend(testS.set_vlan(None,'10', '10.0.0.0 255.0.0.0'))
all_cmd.extend(testS.set_port_vlan('fa 1/1', '10'))
all_cmd.extend(testS.set_static_trunking('fa 0/1', None))
for e in all_cmd:
    print(e)

print('\nS2\n')
testS = Switch()
testR = Router()
all_cmd = []
all_cmd.extend(testS.house_keeping('S2', 'hello', 'student', 'cisco123', 'cisco'))
all_cmd.extend(testS.set_vlan(None,'11', '11.0.0.0 255.0.0.0'))
all_cmd.extend(testS.set_port_vlan('fa 1/1', '11'))
all_cmd.extend(testS.set_static_trunking('fa 0/1', None))
for e in all_cmd:
    print(e)


print('\nrouter\n')
all_cmd = []
all_cmd.extend(testR.house_keeping('R1','hello', 'student', 'cisco123', 'cisco'))
all_cmd.extend(testR.set_dotq_ports_and_dhcp('fa 0/0', '10', '10.0.0.1', '255.0.0.0'))
all_cmd.extend(testR.set_dotq_ports_and_dhcp('fa 1/0', '11', '11.0.0.1', '255.0.0.0'))
all_cmd.extend(testR.static_routing([['11.0.0.0 255.0.0.0', '11.0.0.1']]))
all_cmd.extend(testR.static_routing([['10.0.0.0 255.0.0.0', '10.0.0.1']]))

for e in all_cmd:
    print(e)



