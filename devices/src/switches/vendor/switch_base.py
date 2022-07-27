import os
from datetime import timedelta
import devices.src.mongodb.mongo_device as mongo
from devices.src.layer7.snmp_functions import SnmpFunctions
from devices.src.layer7.network_tools import NetworkTools
import re
from colorama import Fore
from devices.database import path_of_files as path


class SwitchBase:

    def __init__(self, ip: str):
        self.ip = ip
        # conecta no banco para conseguir informações do dispositivo
        db = mongo.Mongo()
        self.__db = db.select_device(ip)
        try:
            # para acesso snmp
            self.community = self.get_community
            self.version = self.get_snmp_version
            self.snmp = SnmpFunctions(self.ip, self.community, self.version)
        except KeyboardInterrupt:
            print("Cancelado pelo administrador")

    @property
    def get_community(self) -> str:
        return self.__db['community']

    @property
    def get_patrimony(self):
        return self.__db['patrimony']

    @property
    def get_location(self):
        return self.__db['location']

    @property
    def get_vendor(self):
        return self.__db['vendor']

    @property
    def get_snmp_version(self):
        return self.__db['snmp_version']

    @property
    def get_model(self):
        return self.__db['model']

    @property
    def get_ports_mac(self):
        return self.__db['ports_mac']

    @property
    def get_name(self):
        return self.__db['name']

    @property
    def get_sysname(self):
        sysname = self.__db['name'].split('.net')[0]
        # sysname = sysname[:len(sysname) - len(sysname.split('.').pop())]
        return sysname

    @property
    def get_patrimony_by_snmp(self):
        try:
            resp = self.snmp.snmp_get("sysContact.0")
        except:
            resp = None
        return resp

    @property
    def get_location_by_snmp(self):
        try:
            resp = self.snmp.snmp_get("sysLocation.0")
        except:
            resp = None
        return resp

    @property
    def get_vendor_by_snmp(self):
        try:
            resp = self.snmp.snmp_get("sysDescr.0")
        except:
            resp = None
        return resp

    @property
    def get_uptime_by_snmp(self):
        try:
            uptime = self.snmp.snmp_get("sysUpTimeInstance")
            # convert para tipo tempo, e para string, para excluir os milisegundos
            seconds = int(uptime) / 100
            up_time = timedelta(seconds=seconds)
            resp = str(up_time).split(".")[0]
        except:
            resp = None
        return resp

    def get_vlan_by_snmp(self):
        resp = self.snmp.snmp_walk(
            "Q-BRIDGE-MIB::dot1qVlanStaticUntaggedPorts")
        vlans: list = []
        for r in resp:
            if r != None:
                vlans.append(r.oid_index)
        return vlans

    def get_lldp_by_snmp(self):
        neig_port = self.snmp.snmp_walk("1.0.8802.1.1.2.1.4.1.1.7")
        neig_sysname = self.snmp.snmp_walk("1.0.8802.1.1.2.1.4.1.1.9")

        port: list = []
        for r in neig_port:
            if r != None:
                new_port = self.parser_port(r.value)
                port.append(new_port)

        sysname: list = []
        for r in neig_sysname:
            if r != None:
                sysname.append(r.value)

        dict_lldp = {}
        dict_lldp['port'] = port
        dict_lldp['sysname'] = sysname

        return dict_lldp

    def get_interfaces_by_snmp(self):
        try:
            walk = self.snmp.snmp_walk('ifName')
        except SystemError:
            print(f"Algo deu errado com o SNMP. Verifique a conectividade com o dispositivo que está tentando acessar")
            return None
        resp: list = []
        for item in walk:
            line = {
                'oid_index': item.oid_index,
                'value': item.value
            }
            resp.append(line)
        return resp

    def get_mac_table(self):
        self.create_template_st()
        snmp = SnmpFunctions(self.ip, self.community,
                             self.version, sprint_value=True)
        try:
            macs = snmp.snmp_walk('.1.3.6.1.2.1.17.4.3.1.1')
        except SystemError:
            print(f"Algo deu errado com o SNMP. Verifique a conectividade com o dispositivo que está tentando acessar")
            return None
        port_fdb_list: list = []
        mac_fdb_list: list = []

        # busca as portas do template

        for mac in macs:
            mac_format = NetworkTools.format_mac(mac.value)
            mac_fdb_list.append(mac_format)

        # busca do banco para saber a quantidade de portas
        db_ports = self.get_ports_mac
        try:
            qtd_ports = len(db_ports)
        except TypeError:
            qtd_ports = 0

        ports_dict: dict = {}
        # inicializa o dict de portas
        for port in db_ports:
            port_no_char = "".join(re.findall("\d+", port))
            ports_dict[port_no_char] = ''

        for i in range(len(port_fdb_list)):
            port = str(port_fdb_list[i])
            if port != '':
                try:
                    if ports_dict[port] == '':
                        ports_dict[port] = mac_fdb_list[i]
                    else:
                        try:
                            ports_dict[port] = str(
                                ports_dict[port]) + '_' + mac_fdb_list[i]
                        except IndexError:
                            pass
                except:
                    try:
                        print(
                            f'erro de chave: {port}, ip: {self.ip}, mac: {mac_fdb_list[i]}')
                    except IndexError:
                        pass
            i += 1

        response: dict = {}
        for key, value in ports_dict.items():
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

    def get_mac_switch_by_snmp(self):
        net = NetworkTools
        snmp = SnmpFunctions(self.ip, self.community,
                             self.version, sprint_value=True)
        try:
            mac = snmp.snmp_get('.1.3.6.1.2.1.2.2.1.6.1007')
            if mac == '0:0:0:0:0:0' or 'No Such' in mac:
                # esse if é para tornar o processo mais rápido.
                # tirando isso, ele não é necessário
                # é menos custoso (em termos de tempo) testar com if do que buscar na rede
                mac = snmp.snmp_get('.1.3.6.1.2.1.2.2.1.6.1')
                if mac == '0:0:0:0:0:0' or 'No Such' in mac:
                    mac = snmp.snmp_get('.1.3.6.1.2.1.2.2.1.6.20')

                    if mac == '0:0:0:0:0:0' or 'No Such' in mac:
                        mac = snmp.snmp_get('.1.3.6.1.2.1.2.2.1.6.49153')

                        if mac == '0:0:0:0:0:0' or 'No Such' in mac:
                            mac = snmp.snmp_get('.1.3.6.1.2.1.2.2.1.6.518')

                            if mac == '0:0:0:0:0:0' or 'No Such' in mac:
                                mac = snmp.snmp_get('.1.3.6.1.2.1.17.1.1.0')

        except SystemError:
            print(f"Algo deu errado com o SNMP. Verifique a conectividade com o dispositivo que está tentando acessar")
            return None
        # except TypeError:
        #    print(f"Cancelado pelo administrador")
        #    return None

        try:
            # se não entrar nos ifs anteriores, esse aqui resolve qualquer caso.
            # Porém, é mais lento, porque busca um atabela interira da mib
            # portanto demora mais
            if mac == "None" or mac == '0:0:0:0:0:0' or 'No Such' in mac:
                macs = snmp.snmp_walk('.1.3.6.1.2.1.2.2.1.6')

                for mac in macs:
                    if mac.value != '0:0:0:0:0:0':
                        return net.format_mac(mac.value)

        except SystemError:
            print(f"Algo deu errado com o SNMP. Verifique a conectividade com o dispositivo que está tentando acessar")
            return None

        return net.format_mac(mac)

    def parser_port(self, port: str) -> str:

        # testa se tem Giga no nome
        if "Gi" in port or "gi" in port or 'Giga' in port or 'giga' in port:
            # GigabitEthernet1/0/48
            new_port = 'Gi' + \
                re.findall(r'[0-9]{1,2}', port, flags=re.IGNORECASE)[-1]
        # testa se é 10 Gb
        elif 'ten' in port or 'Ten' in port or 't' in port or 'te' in port or 'Te' in port:
            new_port = 'Te' + \
                re.findall(r'[0-9]{1,2}', port, flags=re.IGNORECASE)[-1]
        else:
            new_port = re.findall(r'[0-9]{1,2}', port, flags=re.IGNORECASE)[-1]

        return new_port

    def backup_configuration(self):
        print(Fore.RED + "Ainda não implementado para essa marca/modelo de switch!!" + Fore.RESET)
        return False

    def get_neighbour(self):
        print(Fore.RED + "Ainda não implementado para essa marca/modelo de switch!!" + Fore.RESET)
        return False

    def set_ntp(self):
        print(Fore.RED + "Ainda não implementado para essa marca/modelo de switch!!" + Fore.RESET)
        return False

    def set_lldp(self):
        print(Fore.RED + "Ainda não implementado para essa marca/modelo de switch!!" + Fore.RESET)
        return False

    def create_template_st(self):
        vendor = self.get_vendor
        model = self.get_model
        path_dir = path.dir_templates_st + '/' + vendor + '_' + model + '.cfg'
        # cria arquivo, se não existe
        exist = os.path.exists(path_dir)
        if exist is False:
            print(f"Marca: {vendor}, Modelo:{model}")
            with open(path_dir, 'w') as file:
                file.write('[' + model + ']\n')
                file.write('    [[range_ports]]\n')
                interfaces = self.get_interfaces_by_snmp()
                for interface in interfaces:
                    if vendor == 'HP':
                        if model == '1920-48G' or model == '1920-24G':
                            # print(interface['value'])
                            if 'GigabitEthernet' in interface['value']:
                                number = interface['value'].split('/')[-1]
                                name = 'GE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                        elif model == 'V1905-48':
                            if 'Ethernet' in interface['value']:
                                number = interface['value'].split('/')[-1]
                                name = 'FE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})
                        elif model == 'V1910-24G':
                            if 'GigabitEthernet' in interface['value']:
                                number = interface['value'].split('/')[-1]
                                name = 'GE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                    elif vendor == 'Aruba':
                        if model == '2530-24G' or model == '2530-48G' or model == '2930F-48G-4SFP+':
                            if 'lo' not in interface['value'] and 'DEFAULT' not in interface['value']:
                                number = interface['value'].split('/')[-1]
                                name = 'FE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                    elif vendor == 'Cisco':
                        if model == 'SF300-24' or model == 'SF300-48':
                            if 'fa' in interface['value']:
                                number = interface['value'].split('fa')[1]
                                name = 'FE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                        elif model == 'SG300-28PP':
                            if 'gi' in interface['value'] and 'int' not in interface['value']:
                                number = interface['value'].split('gi')[1]
                                name = 'GE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                    elif vendor == 'Dell':
                        if model == 'N1524':
                            if 'Gi' in interface['value']:
                                number = interface['value'].split('/')[-1]
                                name = 'GE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                    elif vendor == 'D-Link':
                        if model == 'DES-1210-28':
                            if 'Slot' in interface['value']:
                                number = interface['value'].split('/')[-1]
                                name = 'FE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                        elif model == 'DES-3028' or model == 'DES-3028P' or model == 'DES-3052' or model == 'DES-3200' or \
                                model == 'DES-3226L' or model == 'DES-3250TG' or model == 'DES-3526' or model == 'DES-3528' or \
                                model == 'DES-3550' or model == 'DGS-3324SRi':
                            if '802' not in interface['value'] and 'System' not in interface['value']:
                                number = interface['value'].split('/')[-1]
                                name = 'FE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                        elif model == 'DGS-3224TGR':
                            if '802' not in interface['value'] and 'System' not in interface['value']:
                                number = interface['value']
                                name = 'FE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                    elif vendor == 'Edge-Core':
                        if model == 'ECS2000-26T':
                            if 'Port' in interface['value']:
                                number = interface['value'].split(' ')[1]
                                name = 'FE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                    elif vendor == 'ExtremeXOS':
                        if model == 'X450a-24t' or model == 'X450e-48p' or model == 'X460G2-24x-10G4':
                            if ':' in interface['value']:
                                number = interface['value'].split(':')[1]
                                name = 'GE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                    elif vendor == 'Huawei':
                        if model == 'S5720-28X-LI-AC' or model == 'S5720-28X-PWR-LI-AC' or model == 'S5720-52X-LI-AC':
                            if 'XGiga' in interface['value'] and 'Loop' not in interface['value'] \
                                    and 'NULL' not in interface['value'] and 'GE0' not in interface['value'] \
                                    and 'Vlan' not in interface['value']:
                                number = interface['value'].split('/')[-1]
                                name = 'TE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})
                            elif 'Giga' in interface['value'] and 'Loop' not in interface['value'] \
                                    and 'NULL' not in interface['value'] and 'GE0' not in interface['value'] \
                                    and 'Vlan' not in interface['value']:
                                number = interface['value'].split('/')[-1]
                                name = 'GE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                    elif vendor == 'SMC':
                        if model == 'SMC6128L2':
                            if 'Port' in interface['value']:
                                number = interface['value'].split('Port')[1]
                                name = 'FE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                    elif vendor == 'TP-Link':
                        if model == 'tplink':
                            if 'port' in interface['value']:
                                number = interface['value'].split(
                                    ':')[0].split(' ')[1]
                                name = 'FE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                        elif model == 'JetStream':
                            if 'fast' in interface['value']:
                                number = interface['value'].split(
                                    ':')[0].split('/')[-1]
                                name = 'FE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})
                            elif 'giga' in interface['value']:
                                number = interface['value'].split(
                                    ':')[0].split('/')[-1]
                                name = 'GE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                    elif vendor == '3com':
                        if model == '2226-SFP' or model == '2250-SFP':
                            if 'Ethernet' in interface['value']:
                                number = interface['value'].split('/')[-1]
                                name = 'FE' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})
                            elif 'Fiber' in interface['value']:
                                number = interface['value'].split('/')[-1]
                                name = 'Fi' + number
                                oid = interface['oid_index']
                                file.write(f'        {oid} = {name}\n')
                                print({oid: name})

                    else:
                        print(
                            f'Erro ao criar template para o fabricante/modelo: {vendor} {model}')


if __name__ == "__main__":
    sb = SwitchBase('192.168.22.215')
    resp = sb.get_mac_switch_by_snmp()
    print(resp)
