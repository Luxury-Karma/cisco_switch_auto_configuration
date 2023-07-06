def house_keeping(self, machine_name: str, banner_message: str, username: str, password: str, secret: str):
    return [f'enable secret {secret}', f'hostname {machine_name}', f'banner {banner_message}',
            f'username {username} password {password}', ]
