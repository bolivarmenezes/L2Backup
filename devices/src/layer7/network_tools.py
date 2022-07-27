import socket
import os
import subprocess
from devices.src.layer7.create_threads import create_threads
from colorama import Fore
from devices.src.mongodb.mongo_device import Mongo
from devices.src.mongodb.mongo_reports import Mongo as MongoReports


class NetworkTools:

    @staticmethod
    def get_my_ip():
        """
        :return:retorna o endereço de ip da própria máquina
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        return s.getsockname()[0]

    @staticmethod
    def status_device(ip):
        """
        :return: retorna 1 se está pingando e 0 se não está
        """
        result = os.system(f'ping -c 1 -W 2 {ip} > /dev/null')
        # a função os.system retorna 0 quando tudo da certo :D
        if result == 0:
            return 1
        return 0

    @staticmethod
    def status_all_gateways():
        dict_all: dict = {}
        dict_all["CPD"] = "192.168.2.1"
        dict_all["Reitoria"] = "192.168.3.1"
        dict_all["CEFD"] = "192.168.4.1"
        dict_all["CAL"] = "192.168.5.1"
        dict_all["CCR42"] = "192.168.6.1"
        dict_all["CCR44"] = "192.168.7.1"
        dict_all["BASE"] = "192.168.8.1"
        dict_all["CE"] = "192.168.9.1"
        dict_all["CCNE"] = "192.168.10.1"
        dict_all["CTLAB"] = "192.168.11.1"
        dict_all["CT"] = "192.168.12.1"
        dict_all["ParqueTec"] = "192.168.13.1"
        dict_all["CCS"] = "192.168.14.1"
        dict_all["CTISM"] = "192.168.15.1"
        dict_all["Biblio"] = "192.168.16.1"
        dict_all["CASM"] = "192.168.17.1"
        dict_all["CCSH"] = "192.168.18.1"
        dict_all["CEU2"] = "192.168.19.1"
        dict_all["CEU1"] = "192.168.20.65"
        dict_all["CCSH2"] = "192.168.22.1"
        dict_all["ODONTO"] = "192.168.27.1"
        dict_all["FONO"] = "192.168.27.65"
        dict_all["CCSH-CCR"] = "192.168.30.29"
        dict_all["UFSM"] = "192.168.33.82"
        dict_all["MGMT"] = "192.168.35.1"
        dict_all["COPERVES"] = "192.168.63.254"
        dict_all["CC"] = "192.168.103.1"
        dict_all["PATRIMONIO"] = "192.168.152.245"
        dict_all["BASE2"] = "192.168.154.1"
        dict_all['NTE'] = "192.168.182.1"
        dict_all['LARP'] = "192.168.183.240"
        dict_all['P67'] = "192.168.184.240"
        dict_all["INPE"] = "192.168.232.11"

        list_gateway: list = []
        for name in dict_all:
            ip = dict_all[name]
            test = NetworkTools.status_device(ip)

            if test == 0:
                # se testar que está fora, testa novamente, só pra garantir :D
                ip = dict_all[name]
                test = NetworkTools.status_device(ip)

            if test == 0:
                # se testar que está fora, testa novamente, só pra garantir :D
                ip = dict_all[name]
                test = NetworkTools.status_device(ip)

            if test == 1:
                print(Fore.BLUE + f"Online --> {name} {ip}")
                ip = ip[:len(ip) - len(ip.split('.').pop())]
                list_gateway.append(ip)
            else:
                print(Fore.RED + f"Offline --> {name} {ip}")
                print(Fore.RESET)
        return list_gateway

    def status_all_devices(self):
        # testa todos os IPs
        ip_list = self.ip_list()
        create_threads(ip_list, self.status_devices)

        #testa novamente os IPs off, só pra garantir
        ip_list = self.ip_list_off()
        create_threads(ip_list, self.status_devices)

        # salvar o a data/hora do último scan
        dbReports = MongoReports()
        dbReports.update_date_last_ping()

    def ip_list(self):
        try:
            db = Mongo()
            devices = db.select_all_devices()
        except:
            print("Verifique o servidor MongoDB")
            return "Erro no banco"
        ip_list: list = []

        for device in devices:
            if device['disable_st'] == '0':
                ip_list.append(device['ip'])
        return ip_list

    def ip_list_off(self):
        try:
            db = Mongo()
            devices = db.select_all_devices()
        except:
            print("Verifique o servidor MongoDB")
            return "Erro no banco"
        ip_list: list = []

        for device in devices:
            if device['online'] == '0':
                ip_list.append(device['ip'])
        return ip_list

    def format_mac(mac: str) -> str:
        new_mac = mac.upper()
        if ':' not in new_mac:
            new_mac = new_mac.replace(' ', ':')
        else:
            new_mac = new_mac.strip()

        # testa se o MAC está com tamanho ok
        if len(new_mac) == 17:
            return new_mac
        # se for diferente de 17, quebra o MAC em 6 octetos
        elif len(new_mac) < 17:
            mac_sliced = new_mac.split(":")
            new_line = ''
            for line in mac_sliced:
                if len(line) == 2:
                    new_line = new_line + line + ':'
                else:
                    new_line += '0' + line + ':'

            # remove, se houver, os dois pontos nos final do arquivo
            if new_line[-1] == ':':
                new_line = new_line[:-1]
                return new_line

            return new_mac

    @staticmethod
    def get_hostname_by_ip(ip: str):
        hostname = os.popen('host ' + ip)
        hostname = hostname.read().split(' ')[-1].strip()
        return hostname[:-1]

    @staticmethod
    def get_ip_by_hostname(hostname: str = 'NaN'):
        """
        hostname: parâmetro de busca para o DNS
        Se não passar o nome como parâmetro, será buscado todos os nomes
        """

        if hostname == 'NaN':
            db = MongoDHCP()
            devices = db.select_all_devices()
            for device in devices:
                try:
                    name = device['dhcp_name']
                    ip = os.popen('host ' + name)
                    ip = ip.read().split(' ')[-1].strip()
                    print(f"Nome: {name}")
                    print(f"IP: {ip}")
                    if 'NXDOMAIN' not in ip:
                        db.update_device({'dhcp_name': name}, {'dhcp_ip': ip})
                    else:
                        db.update_device({'dhcp_name': name}, {'dhcp_ip': 'NaN'})
                except KeyboardInterrupt:
                    print("Interrompido pelo administrador")
                    return None
        else:
            db = MongoDHCP()
            devices = db.select_all_devices()
            try:
                ip = os.popen('host ' + hostname)
                ip = ip.read().split(' ')[-1].strip()
                print(f"Nome: {hostname}")
                print(f"IP: {ip}")
                if 'NXDOMAIN' not in ip:
                    db.update_device({'dhcp_name': hostname}, {'dhcp_ip': ip})
                else:
                    db.update_device({'dhcp_name': hostname}, {'dhcp_ip': 'NaN'})
            except KeyboardInterrupt:
                print("Interrompido pelo administrador")
                return None
            return ip

    @staticmethod
    def network_address(ip):
        return ip[:len(ip) - len(ip.split('.').pop())][:-1]

    @staticmethod
    def status_devices(ip):
        try:
            db = Mongo()
        except:
            print("Verifique o servidor MongoDB")
            return "Erro no banco"
        try:
            status = subprocess.call(f'ping {ip} -c 1 -W 2', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                     shell=True)
        except KeyboardInterrupt:
            status = 1
            pass

        if status == 0:
            # adciona 1 nos status
            print(Fore.BLACK + f"IP: {ip} Status: 1" + Fore.RESET)
            db.update_device({'ip': ip}, {'online': '1'})
        else:
            print(Fore.RED + f"IP: {ip} Status: 0" + Fore.RESET)
            db.update_device({'ip': ip}, {'online': '0'})


if __name__ == "__main__":
    vt = NetworkTools()
    vt.status_all_devices()
