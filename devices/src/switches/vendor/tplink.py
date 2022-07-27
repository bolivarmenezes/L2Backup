import netmiko
from devices.src.switches.switch import Switch
import paramiko.ssh_exception
import re
import devices.database.path_of_files as path_pass
from colorama import Fore


class Tplink(Switch):
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
        for item in walk:
            # print(f'OID: {item.oid}  oid_index: {item.oid_index}  snmp_type: {item.snmp_type}  value: {item.value}')
            # normaliza o nome
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
        pass """

    def backup_configuration(self):
        host = self.ip
        username = 'admin'
        password = path_pass.ST_DEFAULT
        name = self.get_name()
        sysname = self.get_sysname()
        model = self.get_model()
        vendor = self.get_vendor()
        name_backup = self.name_bkp(sysname, vendor, model)

        device = {
            'device_type': 'tplink_jetstream_telnet',
            'host': host,
            'username': username,
            'password': password,
        }
        try:
            print(f"\nConectando ao Switche {host} {name} ...")
            conn = netmiko.ConnectHandler(**device)
            print(f"\nIniciando backup...")
            conn.send_command('enable')
            command = 'copy startup-config tftp ip-address ' + path_pass.telnet_server + ' filename ' + name_backup
            interface = conn.send_command(command)

            print(interface)
            print("########################################################")
            conn.disconnect()
            return True
        except KeyboardInterrupt:
            print(Fore.RED + 'Interrompido pelo Administrador' + Fore.RESET)
            return False
        except netmiko.ssh_exception.NetmikoTimeoutException:
            print(Fore.RED + f'Não foi possível conectar no switch {name}' + Fore.RESET)
            return False
        except netmiko.ssh_exception.NetmikoAuthenticationException:
            print(Fore.RED + f'Senha incorreta para o switch {name}' + Fore.RESET)
            return False
        except paramiko.ssh_exception.AuthenticationException:
            print(Fore.RED + f'Problemas de autenticação no switch {name}' + Fore.RESET)
            return False
        except IndexError:
            print(Fore.RED + f'Problemas de INDEX {name} ?????' + Fore.RESET)
            return False

    def set_ntp(self):
        print("Ainda não implementado para esse modelo")

if __name__ == "__main__":
    s_tplink = Tplink('192.168.27.195')
    resp = s_tplink.get_mac_table()
