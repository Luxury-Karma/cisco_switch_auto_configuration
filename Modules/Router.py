def set_DHCP( dhcp_pool_name: str, ip_address_and_subnet: str):
    return [f'configure terminal', f'ip dhcp pool {dhcp_pool_name}', f'network {ip_address_and_subnet}']


def set_VLAN_DHCP_IPv4( dhcp_pool_name: str, ip_address_and_subnet: str, interface_to_apply: str):
    commands = set_DHCP(dhcp_pool_name, ip_address_and_subnet)
    commands.extend([f'interface {interface_to_apply}',
                     f'ip address {ip_address_and_subnet}',
                     f'ip address dhcp server {dhcp_pool_name}',
                     'no shutdown', 'exit'])
    return commands


def set_VLAN_DHCP_IPv6( dhcp_pool_name: str, ipv6_address_and_prefix: str, interface_to_apply: str):
    return [f'end', f'configure terminal', f'ipv6 dhcp pool {dhcp_pool_name}',
            f'address prefix {ipv6_address_and_prefix}', f'interface {interface_to_apply}',
            f'ipv6 address {ipv6_address_and_prefix}',
            f'ipv6 dhcp server {dhcp_pool_name}',
            'no shutdown', 'exit']


def set_ospf(process_id: str, router_id: str, all_route: list[str], area: str):
    base_command = ['end', 'configure terminal', f'router ospf {process_id}', f'router-id {router_id}']
    for e in all_route:
        base_command.append(f'network {e} area {area}')
    base_command.append('exit')
    return base_command


def set_OSPF_on_router_IPV6( process_id: str, router_id: str, all_route: list[str], area: str):
    base_command = ['end', 'configure terminal', f'ipv6 router ospf {process_id}', f'router-id {router_id}']
    for e in all_route:
        base_command.extend(['interface {}'.format(e), f'ipv6 ospf {process_id} area {area}'])
    base_command.append('exit')
    return base_command


def static_routing( ip_route: list[list[str]]):
    base_command = ['end', 'configure terminal']
    for e in ip_route:
        base_command.append(f'ip route {e[0]} {e[1]}')
    base_command.append('exit')
    return base_command


def set_dot1q_ports( interface: str, interface_dot: list[list[str]]):
    commands = [f'interface {interface}', 'no shutdown']
    for el in interface_dot:
        commands.extend(
            [f'interface {interface}.{el[0]}', f'encapsulation dot1Q {el[0]}', f'ip address {el[1].split()[0]}',
             'no shutdown'])
    commands.extend('exit')
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
        f'exit'
    ])
    return command


def set_dot1q_ports_and_dhcp(interface: str, vlan_number, ip, router_ip):
    return [
        f'interface {interface}',
        f'no shutdown',
        '!',
        f'interface {interface}.{vlan_number}',
        f'encapsulation dot1Q {vlan_number}',
        f'ip address {ip}',
        f'no shutdown',
        f'exit',
        '!',
        f'ip dhcp pool VLAN{vlan_number}',
        f'network {ip}',
        f'default-router {router_ip}',
        f'exit'
    ]


def create_access_list(access_list_number: int, permit: bool, source_ip: list[str]):
    permit_or_deny = 'permit' if permit else 'deny'
    access_list_command = f'access-list {access_list_number} {permit_or_deny} {source_ip}'
    return [access_list_command]


def generate_nat_command(nat_type, internal_ip, external_ip, acl=None):
    command = f"ip nat inside source {nat_type} {internal_ip} {external_ip}"
    if acl:
        command += f" {acl}"
    return command


def generate_nat_overload_config(internal_interface, internal_network, external_interface, public_ip, acl_number):
    config = []
    config.extend('conf t')
    # Configure internal interface
    config.append(f"interface {internal_interface}")
    config.append(f"ip address {internal_network}")
    config.append(f'ip nat inside')
    config.append("no shutdown")

    # Configure external interface
    config.append(f"interface {external_interface}")
    config.append(f"ip address {public_ip}")
    config.append("ip nat outside")
    config.append("no shutdown")

    # Configure NAT Overload
    config.append(f"ip nat inside source list {acl_number} interface {external_interface} overload")

    # Configure ACL
    config.append(f"access-list {acl_number} permit {internal_network}")
    config.append(f'exit')

    return config