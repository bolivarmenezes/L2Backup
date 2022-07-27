from devices.src.switches.switch import Switch


class Planet(Switch):
    """ def get_mac_switch_by_snmp(self):
        pass

    def get_lldp_by_snmp(self):
        pass

    def get_mac_table(self):
        pass """

    def get_interfaces_by_snmp(self):
        try:
            walk = self.snmp.snmp_walk('ifPhysAddress')
        except SystemError:
            print(f"Algo deu errado com o SNMP. Verifique a conectividade com o dispositivo que está tentando acessar")
            return None

        resp: list = []
        for item in walk:
            # print(f'OID: {item.oid}  oid_index: {item.oid_index}  snmp_type: {item.snmp_type}  value: {item.value}')
            resp.append(item.oid_index)
        return resp

    """ def get_vlan_by_snmp(self):
        pass """

    def set_ntp(self):
        print("Ainda não implementado para esse modelo")

if __name__ == "__main__":
    s_hp = Planet('192.168.19.3')
    resp = s_hp.get_interfaces_by_snmp()
    print(resp)
