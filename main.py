"""
The goal of this project is to make that with a simple script we can get the output to all switches and router settings
"""







# todo: all the methode to setup any network machine
class General_Network_Machine():
    # Todo: setup the ip for a specific port and be able to be in ipv6 or v4
    def set_ip(self):
        pass


# todo: all the methode to setup a switch
class Switch(General_Network_Machine):

    # Todo: setup a vlan
    def set_vlan(self):
        pass

    # Todo: setup trucking
    def set_trunking(self):
        pass


# todo : all the methode to setup a switch
class Router(General_Network_Machine):
    # todo: setup osfp on the router
    def set_ospf_on_router(self):
        # Router(config)  # router ospf <process-id>
        # Router(config - router)  # network <network-address> <wildcard-mask> area <area-id>
        # Router(config - router)  # interface <interface-name>
        # Router(config - if)  # ip ospf <process-id> area <area-id>
        pass
    pass
