import ipaddress


def house_keeping(machine_name: str, banner_message: str, username: str, password: str, secret: str):
    return [f'enable secret {secret}', f'hostname {machine_name}', f'banner {banner_message}',
            f'username {username} password {password}', ]


def validate_ip(input_string,with_sub_net = True):
    """
    Ensure that the IP and subnet are valid
    :param input_string:
    :return:
    """
    try:
        ip, subnet = None,None
        if with_sub_net:
            ip, subnet = input_string.split()
            ipaddress.IPv4Address(subnet)  # validate subnet

        ipaddress.IPv4Address(ip if ip else input_string)  # validate ip
        return True
    except ValueError:
        print('This is not and ip format x.x.x.x', ' x.x.x.x' if with_sub_net else '')
        return False




