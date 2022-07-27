from devices.src.switches.switch import Switch
import re


class EdgeCore(Switch):
    """ def get_mac_switch_by_snmp(self):
        pass

    def get_lldp_by_snmp(self):
        pass

    def get_mac_table(self):
        pass """

    def get_interfaces_by_snmp(self):
        try:
            walk = self.snmp.snmp_walk('ifName')
        except SystemError:
            print(f"Algo deu errado com o SNMP. Verifique a conectividade com o dispositivo que está tentando acessar")
            return None
        resp: list = []
        linha: str = ''
        for item in walk:
            # print(f'OID: {item.oid}  oid_index: {item.oid_index}  snmp_type: {item.snmp_type}  value: {item.value}')
            # normaliza o nome
            try:
                # if re.search('Ethernet', item.value, re.IGNORECASE):
                linha = re.findall(
                    r'[0-9]{1,2}\/[0-9]{1,2}', item.value, flags=re.IGNORECASE)[0]
                resp.append(linha.split('/')[-1])
            except IndexError:
                pass
        return resp

    """ def get_vlan_by_snmp(self):
        pass
    """
    def set_ntp(self):
        print("Ainda não implementado para esse modelo")

if __name__ == "__main__":
    s_huawei = EdgeCore('192.168.5.5')
    resp = s_huawei.get_interfaces_by_snmp()
    print(resp)
