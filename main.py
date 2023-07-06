"""
The goal of this project is to make that with a simple script we can get the output to all switches and router settings
"""
from Modules import Switch
from Modules import Router
from Modules import General_Machine













print('S1\n')

all_cmd = []
all_cmd.extend(General_Machine.house_keeping('S1', 'hello', 'student', 'cisco123', 'cisco'))
all_cmd.extend(Switch.set_vlan(None, '11', '11.0.0.0 255.0.0.0'))
all_cmd.extend(Switch.set_port_vlan('fa 1/1', '10'))
all_cmd.extend(Switch.set_vlan(None, '12', '12.0.0.0 255.0.0.0'))
all_cmd.extend(Switch.set_port_vlan('fa 2/1', '11'))
all_cmd.extend(Switch.set_static_trunking('fa 0/1', None))
for e in all_cmd:
    print(e)

print('\nS2\n')
all_cmd = []
all_cmd.extend(General_Machine.house_keeping('S2', 'hello', 'student', 'cisco123', 'cisco'))
all_cmd.extend(Switch.set_vlan(None, '13', '13.0.0.0 255.0.0.0'))
all_cmd.extend(Switch.set_port_vlan('fa 1/1', '13'))
all_cmd.extend(Switch.set_vlan(None, '14', '14.0.0.0 255.0.0.0'))
all_cmd.extend(Switch.set_port_vlan('fa 2/1', '14'))
all_cmd.extend(Switch.set_static_trunking('fa 0/1', None))
for e in all_cmd:
    print(e)

print('\nR1\n')

all_cmd = []
all_cmd.extend(Router.set_DHCP('11', '11.0.0.0 255.0.0.0'))
all_cmd.extend(Router.set_DHCP('12', '12.0.0.0 255.0.0.0'))
all_cmd.extend(Router.set_DHCP('13', '13.0.0.0 255.0.0.0'))
all_cmd.extend(Router.set_DHCP('14', '14.0.0.0 255.0.0.0'))
all_cmd.extend(Router.set_OSPF_on_router('1', '1.1.1.1', ['10.0.0.0'], '0', None))

for e in all_cmd:
    print(e)







