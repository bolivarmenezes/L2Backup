import netmiko
from devices.src.switches.switch import Switch
import re
import devices.database.path_of_files as path_pass
from colorama import Fore
#import logging


class Huawei(Switch):

    def get_interfaces_by_snmp(self):
        try:
            walk = self.snmp.snmp_walk('ifName')
        except SystemError:
            print(f"Algo deu errado com o SNMP. Verifique a conectividade com o dispositivo que está tentando acessar")
            return None
        resp: list = []
        linha: str = ''
        for item in walk:
            try:
                if re.search('Ethernet', item.value, re.IGNORECASE):
                    linha = re.findall(
                        r'[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}', item.value, flags=re.IGNORECASE)[0]
                    resp.append(linha.split('/')[-1])
            except IndexError:
                pass
        return resp

    def get_vlan_by_snmp(self):
        resp = self.snmp.snmp_walk("1.3.6.1.4.1.2011.5.25.42.3.1.1.1.1.2")
        vlans: list = []
        new_vlan = 0
        for r in resp:
            if r != 'None' and r != None:
                try:
                    new_vlan = re.findall(
                        r'[0-9]{1,4}', r.value, flags=re.IGNORECASE)[0]
                except IndexError:
                    pass
                vlans.append(new_vlan)
        return vlans

    def remote_access_telnet(self):
        host = self.ip
        username = 'admin'
        password = path_pass.HUAWEI
        name = self.get_name()
        device_type = 'huawei_telnet'

        port = 23
        if host == '192.168.35.6':
            port = 2323

        device = {
            'device_type': device_type,
            'host': host,
            'username': username,
            'password': password,
            'port': port,
        }

        print(f"\nConectando ao Switch {host} {name} ...")
        try:
            conn = netmiko.ConnectHandler(**device)
        except ConnectionRefusedError:
            print("Erro de conexão!")
            return False
        except:
            return False
        return conn

    def remote_access_ssh(self):
        host = self.ip
        username = 'admin'
        password = path_pass.HUAWEI
        name = self.get_name()
        device_type = 'huawei'

        device = {
            'device_type': device_type,
            'host': host,
            'username': username,
            'password': password,
        }
        print(f"\nConectando ao Switch {host} {name} ...")
        try:
            conn = netmiko.ConnectHandler(**device)
        except KeyboardInterrupt:
            print(Fore.RED + 'Interrompido pelo Administrador' + Fore.RESET)
            return False
        return conn

    def backup_configuration(self):
        name = self.get_name()
        sysname = self.get_sysname()
        model = self.get_model()
        vendor = self.get_vendor()
        name_backup = self.name_bkp(sysname, vendor, model)
        #logging.basicConfig(filename='test.log', level=logging.DEBUG)
        #logger = logging.getLogger("netmiko")
        #print(logger)

        try:
            conn = self.remote_access_telnet()
        except:
            print(
                Fore.RED + f'Erro no acesso Telnet do switch {name}' + Fore.RESET)
            return False

        if conn != False:
            print(f"\nIniciando backup...")
        try:
            tftp = self.get_tftp_server()
            command = 'tftp ' + tftp + ' put flash:/vrpcfg.zip ' + name_backup+'.zip'
            print(command)
            conn.send_command(command)
            print("########################################################")
            conn.disconnect()
            return True
        except AttributeError:
            return False

    def set_lldp(self):
        name = self.get_name()
        print(name)
        conn = self.remote_access_telnet()

        if conn != False:
            print(f"\nIniciando a configuração...")
        try:
            print("Enviando comandos...")
            command = "system-view \n " \
                      "snmp-agent mib-view included iso-view iso \n" \
                      "snmp-agent community read public mib-view iso-view \n" \
                      "snmp-agent sys-info version all \n y \n" \
                      "quit \n" \
                      "save \n y \n quit \n"
            conn.send_command(command)
            return True
        except AttributeError:
            return False
        except EOFError:
            print(Fore.GREEN + 'LLDP Server configurado com sucesso!' + Fore.RESET)
        except ConnectionResetError:
            pass
        return False

    def set_ntp(self):
        name = self.get_name()
        # logging.basicConfig(filename='test.log', level=logging.DEBUG)
        # logger = logging.getLogger("netmiko")
        # print(logger)
        conn = False
        try:
            conn = self.remote_access_ssh()
        except netmiko.ssh_exception.NetmikoTimeoutException:
            print(
                Fore.RED + f'Timeout SSH: Não foi possível conectar no switch {name}' + Fore.RESET)
            print(
                Fore.BLUE + f'Tentando conectar no switch {name} via TELNET' + Fore.RESET)
            conn = self.remote_access_telnet()

        if conn != False:
            print(f"\nIniciando a configuração...")
        try:
            print("Enviando comandos...")
            command = "system-view \n " \
                      "clock timezone Brasilia minus 03:00:00 \n" \
                      "ntp-service server disable \n" \
                      "ntp-service ipv6 server disable \n" \
                      "ntp-service unicast-server 127.0.0.1 \n" \
                      "quit \n" \
                      "save \n y \n quit \n"
            conn.send_command(command)
            return True
        except AttributeError:
            return False
        except EOFError:
            print(Fore.GREEN + 'NTP Server atualizado com sucesso!' + Fore.RESET)
        except ConnectionResetError:
            print(Fore.GREEN + 'NTP Server erro ao atualizar!' + Fore.RESET)


if __name__ == "__main__":
    s_huawei = Huawei('192.168.11.2')
    resp = s_huawei.backup_configuration()
