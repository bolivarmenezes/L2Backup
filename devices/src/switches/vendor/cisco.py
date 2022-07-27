from devices.src.layer7.network_tools import NetworkTools
from devices.src.layer7.snmp_functions import SnmpFunctions
from devices.src.switches.switch import Switch
import re
import telnetlib
import devices.database.path_of_files as path_pass
from colorama import Fore
import time


class Cisco(Switch):

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

    def get_mac_table(self):
        snmp = SnmpFunctions(self.ip, self.community, self.version, sprint_value=True)
        print(f"Modelo: {self.model}")
        try:
            macs = snmp.snmp_walk('.1.3.6.1.2.1.17.4.3.1.1')
            ports = snmp.snmp_walk('.1.3.6.1.2.1.17.4.3.1.2')
        except SystemError:
            print(f"Algo deu errado com o SNMP. Verifique a conectividade com o dispositivo que está tentando acessar")
            return None
        port_fdb_list: list = []
        mac_fdb_list: list = []

        for port in ports:
            port_fdb_list.append(port.value)

        for mac in macs:
            mac_format = NetworkTools.format_mac(mac.value)
            mac_fdb_list.append(mac_format)

        # busca do banco para saber a quantidade de portas
        db_ports = self.get_ports_mac
        try:
            qtd_ports = len(db_ports)
        except TypeError:
            qtd_ports = 0

        ports_cisco: dict = {}

        # inicializando os dicionárions, com os identificadores específicos
        # modelo SG300-28PP
        if self.model == 'SG300-28PP':
            ports_cisco['49'] = ''  # 'gi1'
            ports_cisco['50'] = ''  # 'gi2'
            ports_cisco['51'] = ''  # 'gi3'
            ports_cisco['52'] = ''  # 'gi4'
            ports_cisco['53'] = ''  # 'gi5'
            ports_cisco['54'] = ''  # 'gi6'
            ports_cisco['55'] = ''  # 'gi7'
            ports_cisco['56'] = ''  # 'gi8'
            ports_cisco['57'] = ''  # 'gi9'
            ports_cisco['58'] = ''  # 'gi10'
            ports_cisco['59'] = ''  # 'gi11'
            ports_cisco['60'] = ''  # 'gi12'
            ports_cisco['61'] = ''  # 'gi13'
            ports_cisco['62'] = ''  # 'gi14'
            ports_cisco['63'] = ''  # 'gi15'
            ports_cisco['64'] = ''  # 'gi16'
            ports_cisco['65'] = ''  # 'gi17'
            ports_cisco['66'] = ''  # 'gi18'
            ports_cisco['67'] = ''  # 'gi19'
            ports_cisco['68'] = ''  # 'gi20'
            ports_cisco['69'] = ''  # 'gi21'
            ports_cisco['70'] = ''  # 'gi22'
            ports_cisco['71'] = ''  # 'gi23'
            ports_cisco['72'] = ''  # 'gi24'
            ports_cisco['73'] = ''  # 'gi25'
            ports_cisco['74'] = ''  # 'gi26'
            ports_cisco['75'] = ''  # 'gi27'
            ports_cisco['76'] = ''  # 'gi28'
            number_of_ports = 28
        elif self.model == 'SF300-24':
            ports_cisco['1'] = ''  # fa1
            ports_cisco['2'] = ''  # fa2
            ports_cisco['3'] = ''  # fa3
            ports_cisco['4'] = ''  # fa4
            ports_cisco['5'] = ''  # fa5
            ports_cisco['6'] = ''  # fa6
            ports_cisco['7'] = ''  # fa7
            ports_cisco['8'] = ''  # fa8
            ports_cisco['9'] = ''  # fa9
            ports_cisco['10'] = ''  # fa10
            ports_cisco['11'] = ''  # fa11
            ports_cisco['12'] = ''  # fa12
            ports_cisco['13'] = ''  # fa13
            ports_cisco['14'] = ''  # fa14
            ports_cisco['15'] = ''  # fa15
            ports_cisco['16'] = ''  # fa16
            ports_cisco['17'] = ''  # fa17
            ports_cisco['18'] = ''  # fa18
            ports_cisco['19'] = ''  # fa19
            ports_cisco['20'] = ''  # fa20
            ports_cisco['21'] = ''  # fa21
            ports_cisco['22'] = ''  # fa22
            ports_cisco['23'] = ''  # fa23
            ports_cisco['24'] = ''  # fa24
            ports_cisco['49'] = ''  # gi1
            ports_cisco['50'] = ''  # gi2
            ports_cisco['51'] = ''  # gi3
            ports_cisco['52'] = ''  # gi4
            number_of_ports = 28

        elif self.model == 'SF300-48':
            ports_cisco['1'] = ''  # fa1
            ports_cisco['2'] = ''  # fa2
            ports_cisco['3'] = ''  # fa3
            ports_cisco['4'] = ''  # fa4
            ports_cisco['5'] = ''  # fa5
            ports_cisco['6'] = ''  # fa6
            ports_cisco['7'] = ''  # fa7
            ports_cisco['8'] = ''  # fa8
            ports_cisco['9'] = ''  # fa9
            ports_cisco['10'] = ''  # fa10
            ports_cisco['11'] = ''  # fa11
            ports_cisco['12'] = ''  # fa12
            ports_cisco['13'] = ''  # fa13
            ports_cisco['14'] = ''  # fa14
            ports_cisco['15'] = ''  # fa15
            ports_cisco['16'] = ''  # fa16
            ports_cisco['17'] = ''  # fa17
            ports_cisco['18'] = ''  # fa18
            ports_cisco['19'] = ''  # fa19
            ports_cisco['20'] = ''  # fa20
            ports_cisco['21'] = ''  # fa21
            ports_cisco['22'] = ''  # fa22
            ports_cisco['23'] = ''  # fa23
            ports_cisco['24'] = ''  # fa24
            ports_cisco['25'] = ''  # fa25
            ports_cisco['26'] = ''  # fa26
            ports_cisco['27'] = ''  # fa27
            ports_cisco['28'] = ''  # fa28
            ports_cisco['29'] = ''  # fa29
            ports_cisco['30'] = ''  # fa30
            ports_cisco['31'] = ''  # fa31
            ports_cisco['32'] = ''  # fa32
            ports_cisco['33'] = ''  # fa33
            ports_cisco['34'] = ''  # fa34
            ports_cisco['35'] = ''  # fa35
            ports_cisco['36'] = ''  # fa36
            ports_cisco['37'] = ''  # fa37
            ports_cisco['38'] = ''  # fa38
            ports_cisco['39'] = ''  # fa39
            ports_cisco['40'] = ''  # fa40
            ports_cisco['41'] = ''  # fa41
            ports_cisco['42'] = ''  # fa42
            ports_cisco['43'] = ''  # fa43
            ports_cisco['44'] = ''  # fa44
            ports_cisco['45'] = ''  # fa45
            ports_cisco['46'] = ''  # fa46
            ports_cisco['47'] = ''  # fa47
            ports_cisco['48'] = ''  # fa48
            ports_cisco['49'] = ''  # gi1
            ports_cisco['50'] = ''  # gi2
            ports_cisco['51'] = ''  # gi3
            ports_cisco['52'] = ''  # gi4
            number_of_ports = 48

        for i in range(len(port_fdb_list)):
            port = str(port_fdb_list[i])
            if port != '':
                try:
                    if ports_cisco[port] == '':
                        ports_cisco[port] = mac_fdb_list[i]
                    else:
                        try:
                            ports_cisco[port] = str(ports_cisco[port]) + '_' + mac_fdb_list[i]
                        except IndexError:
                            pass
                except KeyError:
                    try:
                        print(f'erro de chave: {port}, ip: {self.ip}, mac: {mac_fdb_list[i]}')
                    except IndexError:
                        pass
            i += 1

        response: dict = {}
        for key, value in ports_cisco.items():
            # adicionar o nome correto da porta
            for port in db_ports:
                port_no_char = "".join(re.findall("\d+", port))
                if key == port_no_char:
                    new_key = port

                    if value == '':
                        response[new_key] = ['NaN']
                    elif '_' in value:
                        response[new_key] = value.split('_')
                    else:
                        response[new_key] = value

        return response

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
                if self.model == 'SF300-24' or self.model == '24-Port 10/100':
                    if re.search('\\bfa', item.value, re.IGNORECASE) or \
                            re.search('\\bgi', item.value, re.IGNORECASE) or \
                            re.search('\\bf', item.value, re.IGNORECASE) or \
                            re.search('\\be', item.value, re.IGNORECASE) or \
                            re.search('\\bg', item.value, re.IGNORECASE):
                        linha = re.findall(
                            r'[0-9]{1,2}', item.value, flags=re.IGNORECASE)[0]
                        resp.append(linha)

                else:
                    if re.search('\\be', item.value, re.IGNORECASE) or \
                            re.search('\\bf', item.value, re.IGNORECASE) or \
                            re.search('\\bg', item.value, re.IGNORECASE):
                        linha = re.findall(
                            r'[0-9]{1,2}', item.value, flags=re.IGNORECASE)[0]
                        resp.append(linha)
            except IndexError:
                pass
        return resp

    def backup_configuration(self):
        host = self.ip
        device_type = 'cisco_ios_telnet'
        username = 'admin'
        password = path_pass.ST_DEFAULT
        name = self.get_name()
        sysname = self.get_sysname()
        model = self.model
        # if model == 'SG300-28PP':
        try:
            print(f"\nConectando ao Switch {host} {name}...")

            t = telnetlib.Telnet(host)  # actively connects to a telnet server
            # t.set_debuglevel(1)  # uncomment to get debug messages
            time.sleep(2)
            t.read_until(b'User Name:', 100)  # waits until it recieves a string 'login:'
            time.sleep(2)
            t.write(username.encode('utf-8'))  # sends username to the server
            t.write(b'\r')  # sends return character to the server
            t.read_until(b'Password:', 100)  # waits until it recieves a string 'Password:'
            t.write(password.encode('utf-8'))  # sends password to the server
            t.write(b'\r')  # sends return character to the server

            print(f"\nIniciando backup...")
            model = self.get_model()
            vendor = self.get_vendor()
            name_backup = self.name_bkp(sysname, vendor, model)
            command = 'copy running-config tftp://' + path_pass.telnet_server + '/' + name_backup
            t.write(command.encode('utf-8') + b'\r')  # sends a command to the server
            t.write(b'\r')
            time.sleep(5)
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