import ipaddress


def house_keeping(machine_name: str, banner_message: str, username: str, password: str, secret: str):
    return [f'enable secret {secret}', f'hostname {machine_name}', f'banner {banner_message}',
            f'username {username} password {password}', ]


def __is_it_an_ip(input_string):
    """
    Ensure that the IP and subnet are valid
    :param input_string:
    :return:
    """
    try:
        ip, subnet = input_string.split()
        ipaddress.IPv4Address(ip)  # validate ip
        ipaddress.IPv4Address(subnet)  # validate subnet
        return True
    except ValueError:
        print('This is not and ip format x.x.x.x x.x.x.x')
        return False


def __ip_in_network(input_string):
    try:
        ip, netmask = input_string.split()
        ip = ipaddress.IPv4Address(ip)
        netmask = ipaddress.IPv4Address(netmask)
        # Create a network from the IP address and netmask
        network = ipaddress.IPv4Network(f"{ip.network.network_address}/{netmask}", strict=False)
        return ip in network
    except ValueError:
        return False


def validate_ip(ip_data: str):
    """
    Receive an ip and subnet and verify if it is one and if it is valide
    :param ip_data:
    :return:
    """
    if __is_it_an_ip(ip_data):
        if __ip_in_network(ip_data):
            return True
    return False


def validate_pure_ip(ip:str):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except Exception as e:
        print('Invalid IP')
        return False