import threading
import time
from devices.src.mongodb.mongo_device import Mongo
from devices.src.switches.switch import Switch
from devices.src.switches.vendor.hp import Hp
from devices.src.switches.vendor.aruba import Aruba
from devices.src.switches.vendor.extreme import Extreme
from devices.src.switches.vendor.dlink import Dlink
from devices.src.switches.vendor.huawei import Huawei
from devices.src.switches.vendor.cisco import Cisco
from devices.src.switches.vendor.threecom import Threecom
from devices.src.switches.vendor.planet import Planet
from devices.src.switches.vendor.edgecore import EdgeCore
from devices.src.switches.vendor.dell import Dell
from devices.src.switches.vendor.smc import Smc
from devices.src.switches.vendor.tplink import Tplink


class CommandsExec:

    def __init__(self, type_of_function: str = 'lldp', ip: str = '0') -> None:
        self.db = Mongo()
        self.many = False
        self.type_of_function = type_of_function

        if ip != '0':
            # se entrar aqui, significa que o IP foi passado
            self.ip = ip
            self._strategy = Switch(self.ip)
            self.device = self.db.select_device(ip)
            self.vendor = self.device['vendor']
            self.community = self.device['community']
            self.snmp_version = self.device['snmp_version']
            self.model = self.device['model']
            self.status = self.device['online']
        else:
            self.many = True

    def vendor_switch(self) -> Switch:
        if self.vendor == 'D-Link':
            self._strategy = Dlink(self.ip)

        elif self.vendor == 'HP':
            self._strategy = Hp(self.ip)

        elif self.vendor == 'Aruba':
            self._strategy = Aruba(self.ip)

        elif self.vendor == 'ExtremeXOS':
            self._strategy = Extreme(self.ip)

        elif self.vendor == 'Huawei':
            self._strategy = Huawei(self.ip)

        elif self.vendor == 'Cisco':
            self._strategy = Cisco(self.ip)

        elif self.vendor == '3com':
            self._strategy = Threecom(self.ip)

        elif self.vendor == 'Edge-Core':
            self._strategy = EdgeCore(self.ip)

        elif self.vendor == 'Dell':
            self._strategy = Dell(self.ip)

        elif self.vendor == 'Planet':
            self._strategy = Planet(self.ip)

        elif self.vendor == 'SMC':
            self._strategy = Smc(self.ip)

        elif self.vendor == 'TP-Link':
            self._strategy = Tplink(self.ip)

        return self._strategy

    def ip_list(self):
        devices = self.db.select_all_devices()
        ip_list: list = []

        for device in devices:
            disable = device['disable_st']
            status = device['online']
            disable_scan = device['disable_scan']
            enable_scan = False
            if disable_scan == '0':
                enable_scan = True

            if disable == '0' and status == '1' and enable_scan:
                ip_list.append(device['ip'])
        return ip_list

    def command_factory(self, functionT):
        if self.many:
            '''
            Se for para executar em todos os switches...
            '''
            ip_list = self.ip_list()
            try:
                '''
                Os parâmetros são: uma lista de IPs e a função a ser executada
                '''
                self.create_threads_commands(ip_list, functionT)

            except KeyboardInterrupt:
                print("Cancelado pelo Administrador")

        else:
            '''
            Se for para executar apenas no switche passado como parâmetro...
            Nesse caso, não é preciso executar em threads
            '''
            try:
                self.command(self.ip)
            except KeyboardInterrupt:
                print("Cancelado pelo Administrador")
                return False
            except FileNotFoundError:
                print("Arquivo de LOG não encontrado")
                return False
            except:
                print("Erro! Tratar no arquivo backup_st_configurations_thread.py")
                return False

    def create_threads_commands(list, function, delay=1):
        threads = []

        for ip in list:
            # args is a tuple with a single element
            th = threading.Thread(target=function, args=(ip,))
            time.sleep(delay)
            th.start()
            threads.append(th)

        for th in threads:
            th.join()

    def command_lldp(self):
        '''
        cria um objeto do que será executado, para passar pra thread
        '''
        st = Switch()
        function_obj = st.set_lldp()
        
        self.create_threads_commands(self.ip_list, function_obj)
        print("Switch LLDP: {name}")



    def command_ntp(self):        
        '''Commando que será executado nos switches'''
        st = Switch()
        function_obj = st.set_ntp()
        
        self.create_threads_commands(self.ip_list, function_obj)
        print("Switch NTP: {name}")
