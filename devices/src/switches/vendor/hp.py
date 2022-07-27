import time
import telnetlib
import devices.database.path_of_files as path_pass
from colorama import Fore
from devices.src.layer7.network_tools import NetworkTools
from devices.src.layer7.snmp_functions import SnmpFunctions
from devices.src.switches.switch import Switch
import re


class Hp(Switch):

    def get_mac_switch_by_snmp(self):
        net = NetworkTools
        snmp = SnmpFunctions(self.ip, self.community, self.version, sprint_value=True)
        mac = str(snmp.snmp_get('.1.3.6.1.2.1.17.1.1.0'))
        if '"' in mac:
            mac = mac.strip('"')[:-1]
        if ':' not in mac:
            mac = mac.replace(' ', ':')
        return net.format_mac(mac)

    def get_lldp_by_snmp(self):
        neig_port = self.snmp.snmp_walk("1.0.8802.1.1.2.1.4.1.1.7")
        neig_sysname = self.snmp.snmp_walk("1.0.8802.1.1.2.1.4.1.1.9")

        dict_lldp = {}
        try:
            port: list = []
            sysname: list = []
            count = 0
            for n in neig_sysname:
                if n != None:
                    if '-' in n.value:
                        name = re.findall(
                            r'[a-z]{2,5}-', n.value, flags=re.IGNORECASE)[0].strip('-')
                        if name == 'st' or name == 'stpoe':
                            sysname.append(n.value)
                            p = neig_port[count].value
                            if p != None:
                                por = re.findall(
                                    r'[0-9]{1,2}', p, flags=re.IGNORECASE)[0]
                                if por != '0':
                                    new_port = self.parser_port(p)
                                    port.append(new_port)
                                    count += 1
        except IndexError:
            pass

        try:
            if len(port) > 0 and len(sysname) > 0:
                dict_lldp['port'] = port
                dict_lldp['sysname'] = sysname
                return dict_lldp
            else:
                return 0
        except UnboundLocalError:
            return 0

    """def get_mac_table(self):
        snmp = SnmpFunctions(self.ip, self.community, self.version, sprint_value=True)

        try:
            macs = snmp.snmp_walk('.1.3.6.1.2.1.17.4.3.1.1')
            ports = snmp.snmp_walk('.1.3.6.1.2.1.17.4.3.1.2')
        except SystemError:
            print(f"Algo deu errado com o SNMP. Verifique a conectividade com o dispositivo que está tentando acessar")
            return None
        port_list: list = []
        mac_list: list = []

        for port in ports:
            port_list.append(port.value)

        for mac in macs:
            mac_format = NetworkTools.format_mac(mac.value)
            mac_list.append(mac_format)
        # passando para um set, os números de portas não repetem

        # busca do banco para saber a quantidade de portas
        qtd_ports = len(self.get_ports_mac)

        result: dict = {}

        # inicializa o dict
        for i in range(qtd_ports):
            result[str(i + 1)] = 0

        for i in range(len(port_list)):
            port = str(port_list[i])
            try:
                if result[port] == 0:
                    result[port] = mac_list[i]
                else:
                    result[port] = result[port] + '_' + mac_list[i]
            except:
                print(f'erro de chave: {port}, ip: {self.ip}')

            i += 1

        resp: dict = {}
        for k, v in result.items():
            print(f'chave: {k} valor: {v}')

            if v == 0:
                resp[k] = ['NaN']
            elif '_' in v:
                resp[k] = v.split('_')
            else:
                resp[k] = v

        return resp"""

    def get_interfaces_by_snmp(self):
        try:
            walk = self.snmp.snmp_walk('ifName')
        except SystemError:
            print(f"Algo deu errado com o SNMP. Verifique a conectividade com o dispositivo que está tentando acessar")
            return None
        resp: list = []
        linha: str = ''

        if self.model == '2530-48G' or self.model == '2530-24G':
            for item in walk:
                # print(f'OID: {item.oid}  oid_index: {item.oid_index}  snmp_type: {item.snmp_type}  value: {item.value}')
                # normaliza o nome
                try:
                    if re.search('lo', item.value, re.IGNORECASE) is None:
                        linha = re.findall(
                            r'[0-9]{1,2}', item.value, flags=re.IGNORECASE)[0]
                        resp.append(linha)
                except IndexError:
                    pass
        else:
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

    def backup_configuration(self):
        host = self.ip
        username = 'admin'
        password = path_pass.ST_DEFAULT
        name = self.get_name()
        sysname = self.get_sysname()
        model = self.get_model()
        vendor = self.get_vendor()
        name_backup = self.name_bkp(sysname, vendor, model)

        # excessões de senha
        if host == '192.168.33.69' or host == '192.168.33.66':
            password = path_pass.EXTREME_2

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

            command = '_cmdline-mode on' + '\rY'
            t.write(command.encode('utf-8') + b'\r')
            time.sleep(3)

            t.read_until(b'Please input password:', 100)
            command = 'Jinhua1920unauthorized'
            t.write(command.encode('utf-8') + b'\r\n')
            time.sleep(3)
            t.write(b'\r')
            command = 'backup startup-configuration to ' + path_pass.telnet_server + ' ' + name_backup
            t.write(command.encode('utf-8') + b'\r')
            t.write(b'\r')

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

    """ def get_vlan_by_snmp(self):
        pass """

    def set_ntp(self):
        print("Ainda não implementado para esse modelo")

if __name__ == "__main__":
    s_hp = Hp('192.168.33.66')
    resp = s_hp.backup_configuration()
    print(resp)
