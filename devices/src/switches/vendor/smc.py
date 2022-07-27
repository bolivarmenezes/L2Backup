from devices.src.switches.switch import Switch
import re
import telnetlib
import time
import devices.database.path_of_files as path_pass
from colorama import Fore


class Smc(Switch):
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
                if re.search('Port', item.value, re.IGNORECASE):
                    linha = re.findall(
                        r'[0-9]{1,2}', item.value, flags=re.IGNORECASE)[0]
                    resp.append(linha.split('/')[-1])
            except IndexError:
                pass
        return resp

    """ def get_vlan_by_snmp(self):
        pass
    """

    def backup_configuration(self):
        host = self.ip
        device_type = 'cisco_ios_telnet'
        username = 'admin'
        password = path_pass.ST_DEFAULT
        name = self.get_name()
        sysname = self.get_sysname()
        model = self.get_model()
        vendor = self.get_vendor()
        name_backup = self.name_bkp(sysname, vendor, model)
        try:
            print(f"\nConectando ao Switch {host} {name}...")

            t = telnetlib.Telnet(host)  # actively connects to a telnet server
            # t.set_debuglevel(1)  # uncomment to get debug messages
            time.sleep(2)
            t.read_until(b'Username:', 100)  # waits until it recieves a string 'login:'
            time.sleep(2)
            t.write(username.encode('utf-8'))  # sends username to the server
            t.write(b'\r')  # sends return character to the server
            t.read_until(b'Password:', 100)  # waits until it recieves a string 'Password:'
            t.write(password.encode('utf-8'))  # sends password to the server
            t.write(b'\r')  # sends return character to the server

            print(f"\nIniciando backup...")

            command = 'copy startup-config tftp'
            t.write(command.encode('utf-8') + b'\r')

            command = path_pass.telnet_server
            t.write(command.encode('utf-8') + b'\r')

            command = name_backup
            t.write(command.encode('utf-8') + b'\r')

            t.write(b'\n\r')
            t.write(b'exit\n')
            time.sleep(1)
            t.write(b'\r')  # sends a command to the server
            t.close()

            print("Backup Concluído")
            print("########################################################")
            return True
        except:
            print(Fore.RED + f'Sem conectividade com: {name} Verificar telnet' + Fore.RESET)
            return False

    def set_ntp(self):
        print("Ainda não implementado para esse modelo")

if __name__ == "__main__":
    s_huawei = Smc('192.168.12.21')
    resp = s_huawei.get_interfaces_by_snmp()
    print(resp)
