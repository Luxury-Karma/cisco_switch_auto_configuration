def set_vlan( vlan_name: str, vlan_number: str, vlan_ip: str):
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


def set_port_vlan( interface: str, vlan_number: str):
    """
    Set the vlan for the interface
    :param interface: wich interface is to setup
    :param vlan_number: wich vlan is suppose to handle it
    :return: the command to give a vlan to a interface
    """
    return [f'interface {interface}', f'switchport access vlan {vlan_number}']


def set_static_trunking( port_to_trunk: str, vlan_to_allow: list[str] or None):
    """
    Make a static trunk in the vlan
    :param port_to_trunk: witch interface we need to make a trunk
    :param vlan_to_allow: wich vlan are allowed (if empty all)
    :return:
    """
    vlan_to_allow = vlan_to_allow if vlan_to_allow else ['all']
    command = [f'interface {port_to_trunk}', f'switchport mode trunk']
    if 'all' not in vlan_to_allow:
        for e in vlan_to_allow:
            command.extend(f'switchport trunk allowed vlan {e}')
    return command


def set_dynamic_trunking_desirable(port_to_trunk: str):
    """
    Create a dynamic desirable trunk.
    :param port_to_trunk: Wich port will be the desirable trunk
    :return: the command to do it
    """
    return [f'interface {port_to_trunk}', 'switchport mode dynamic desirable']


def set_dynamic_trunking_auto( port_to_trunk: str):
    """
    Create a dynamic auto trunk
    :param port_to_trunk: wich port to trunk
    :return: the command to do it
    """
    return [f'interface {port_to_trunk}', 'switchport mode dynamic auto']


