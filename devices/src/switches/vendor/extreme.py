from devices.src.switches.switch import Switch
import time
import re
import devices.database.path_of_files as path_pass
from colorama import Fore
import netmiko
#import logging
#from devices.src.layer7.file_tools import FileTools as file_tools


class Extreme(Switch):
    """def get_mac_switch_by_snmp(self):
        pass

    def get_lldp_by_snmp(self):
        pass

    def get_mac_table(self):
        pass
    """

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
                linha = re.findall(
                    r'[0-9]{1,2}\:[0-9]{1,2}', item.value, flags=re.IGNORECASE)[0]
                resp.append(linha.split(':')[-1])
            except IndexError:
                pass
        return resp

    def get_vlan_by_snmp(self):
        resp = self.snmp.snmp_walk("1.3.6.1.4.1.1916.1.2.1.2.1.10")
        vlans: list = []
        for r in resp:
            if r != 'None':
                new_vlan = re.findall(
                    r'[0-9]{1,4}', r.value, flags=re.IGNORECASE)[0]
                vlans.append(new_vlan)
        return vlans

    def backup_configuration(self):
        host = self.ip
        username = 'admin'
        password = path_pass.EXTREME_1
        name = self.get_name()
        sysname = self.get_sysname()

        #logName = path_pass.logs_dir+host+'_'+sysname+'.log'
        #file_tools.create_file_if_no_exist(logName)
        #logging.basicConfig(filename=logName, level=logging.DEBUG)
        #logger = logging.getLogger("netmiko")
        #print(logger)

        if host == '192.168.8.11' or host == '192.168.2.129' or host == '192.168.33.104':
            password = path_pass.EXTREME_2
        elif host == '192.168.33.104' or host == '192.168.33.82' or host == '192.168.35.5':
            password = path_pass.EXTREME_3

        device = {
            'device_type': 'extreme_exos_telnet',
            'host': host,
            'username': username,
            'password': password,
            'port': 2323,
        }
        try:
            print(f"\nConectando ao Switche {host} {name}...")
            conn = netmiko.ConnectHandler(**device)
            #print(device)
            print(f"\nIniciando backup...")
            model = self.get_model()
            vendor = self.get_vendor()
            name_backup = self.name_bkp(sysname, vendor, model)
            tftp = self.get_tftp_server()
            command = 'upload configuration ' + tftp + ' ' + name_backup + ' vr VR-Default'
            if host == '192.168.35.13':
                name_backup = self.name_bkp('st-ufsm-09a', vendor, model)
                command = 'upload configuration ' + tftp + ' ' + name_backup + ' vr VR-Mgmt'

            if host == '192.168.35.19':
                name_backup = self.name_bkp('st-ufsm-09b', vendor, model)
                command = 'upload configuration ' + tftp + ' ' + name_backup + ' vr VR-Mgmt'

            if host == '192.168.35.5':
                name_backup = self.name_bkp('st-cloud-00', vendor, model)
                command = 'upload configuration ' + tftp + ' ' + name_backup + ' vr VR-Mgmt'

            print(command)
            conn.send_command(command)
            #if host == '192.168.33.108' or host == '192.168.33.107' or host == '192.168.33.102':
            time.sleep(5)
            print("Concluído\n########################################################")
            conn.disconnect()
            return True
        except KeyboardInterrupt:
            print(Fore.RED + 'Interrompido pelo Administrador' + Fore.RESET)
            return False
        except netmiko.ssh_exception.NetmikoTimeoutException:
            print(Fore.RED + f'Não foi possível conectar no switch {name} ' + Fore.RESET)
            return False
        except netmiko.ssh_exception.NetmikoAuthenticationException:
            print(Fore.RED + f'Senha incorreta para o switch {name}' + Fore.RESET)
            return False
        except OSError:
            print(Fore.RED + f'Sem conectividade com o {name}' + Fore.RESET)
            return False
    def set_ntp(self):
        print("Ainda não implementado para esse modelo")

if __name__ == "__main__":
    s_exos = Extreme('192.168.33.72')
    resp = s_exos.backup_configuration()
    print(resp)
