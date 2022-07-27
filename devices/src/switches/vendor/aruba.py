import netmiko
import devices.database.path_of_files as path_pass
from devices.src.switches.switch import Switch
import re
from colorama import Fore
from devices.src.layer7.network_tools import NetworkTools
from devices.src.layer7.snmp_functions import SnmpFunctions
import logging


class Aruba(Switch):

    def get_mac_switch_by_snmp(self):
        net = NetworkTools
        snmp = SnmpFunctions(self.ip, self.community, self.version, sprint_value=True)
        mac = str(snmp.snmp_get('.1.3.6.1.2.1.17.1.1.0'))
        if '"' in mac:
            mac = mac.strip('"')[:-1]
        if ':' not in mac:
            mac = mac.replace(' ', ':')
        return net.format_mac(mac)

    """def get_lldp_by_snmp(self):
        return "Chegou onde devia"

    def get_mac_table(self):
        pass """

    def get_interfaces_by_snmp(self):
        try:
            walk = self.snmp.snmp_walk('ifName')
        except SystemError:
            print(f"Algo deu errado com o SNMP. Verifique a conectividade com o dispositivo que está tentando acessar")
            return None
        resp: list = []

        if self.model == '2530-48G' or self.model == '2530-24G':
            for item in walk:
                """ 
                print(f'OID: {item.oid}  oid_index: {item.oid_index}  
                snmp_type: {item.snmp_type}  value: {item.value}')
                normaliza o nome
                """
                try:
                    if re.search('lo', item.value, re.IGNORECASE) is None:
                        linha = re.findall(
                            r'[0-9]{1,2}', item.value, flags=re.IGNORECASE)[0]
                        resp.append(linha)
                except IndexError:
                    pass
        else:
            for item in walk:
                """ 
                print(f'OID: {item.oid}  oid_index: {item.oid_index}  
                snmp_type: {item.snmp_type}  value: {item.value}') normaliza o nome
                """
                try:
                    if re.search('Ethernet', item.value, re.IGNORECASE):
                        linha = re.findall(
                            r'[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}', item.value, flags=re.IGNORECASE)[0]
                        resp.append(linha.split('/')[-1])
                except IndexError:
                    pass

        return resp

    """    
    def get_vlan_by_snmp(self):
        pass
    """

    def remote_access(self):
        host = self.ip
        username = 'admin'
        password = path_pass.ST_DEFAULT
        name = self.get_name()

        device = {
            'device_type': 'aruba_os',
            'host': host,
            'username': username,
            'password': password,
        }
        try:
            print(f"\nConectando ao Switche {host} ...")
            try:
                conn = netmiko.ConnectHandler(**device)
            except EOFError:
                print(f'Erro ao conectar no host: {host}')
        except KeyboardInterrupt:
            print(Fore.RED + 'Interrompido pelo Administrador' + Fore.RESET)
            return False
        except netmiko.ssh_exception.NetmikoTimeoutException:
            print(Fore.RED + f'Não foi possível conectar no switch {name}' + Fore.RESET)
            return False
        except netmiko.ssh_exception.NetmikoAuthenticationException:
            print(Fore.RED + f'Senha incorreta para o switch {name}' + Fore.RESET)
            return False
        return conn

    def backup_configuration(self):
        conn = self.remote_access()
        sysname = self.get_sysname()
        model = self.get_model()
        vendor = self.get_vendor()
        name_backup = self.name_bkp(sysname, vendor, model)
        print(f"\nIniciando backup...")
        conn.send_command('save config.cfg')
        interface = conn.send_command(
            'copy startup-config tftp ' + path_pass.telnet_server + ' ' + name_backup)
        print(interface)
        print("Concluído\n########################################################")
        conn.disconnect()
        return True

    def get_neighbour(self):
        conn = self.remote_access()
        print(f"\nBuscando vizinhos...")
        interface = conn.send_command('show lldp info remote-device')
        print(interface)
        conn.disconnect()
        return True

    def set_ntp(self):
        name = self.get_name()
        conn = False
        logging.basicConfig(filename='test.log', level=logging.DEBUG)
        logger = logging.getLogger("netmiko")
        print(logger)
        try:
            conn = self.remote_access()
        except netmiko.ssh_exception.NetmikoTimeoutException:
            print(Fore.RED + f'Timeout SSH: Não foi possível conectar no switch {name}' + Fore.RESET)

        if conn != False:
            print(f"\nIniciando a configuração...")
        try:
            print("Enviando comandos...")
            command = "configure terminal \n" \
                      "timesync ntp \n" \
                      "ntp unicast \n" \
                      "ntp server 127.0.0.1 \n" \
                      "ntp enable \n" \
                      "clock timezone gmt -3:00 \n" \
                      "exit \n" \
                      "save \n"
            conn.send_command(command)
            return True
        except AttributeError:
            return False
        except EOFError:
            print(Fore.GREEN + 'NTP Server atualizado com sucesso!' + Fore.RESET)
        except ConnectionResetError:
            print(Fore.GREEN + 'NTP Server atualizado com sucesso!' + Fore.RESET)


if __name__ == "__main__":
    sb = Aruba('192.168.3.21')
    resp = sb.get_neighbour()
