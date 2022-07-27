from devices.src.layer7.create_threads_bkp import create_threads_bkp
from .mongodb.mongo_device import Mongo
from .switches.switch import Switch
from .switches.vendor.aruba import Aruba
from .switches.vendor.extreme import Extreme
from .switches.vendor.dlink import Dlink
from .switches.vendor.huawei import Huawei
from .switches.vendor.cisco import Cisco
from .switches.vendor.threecom import Threecom
from .switches.vendor.planet import Planet
from .switches.vendor.edgecore import EdgeCore
from .switches.vendor.dell import Dell
from .switches.vendor.smc import Smc
from .switches.vendor.tplink import Tplink
from .switches.vendor.hp import Hp


class LldpSwitch:

    def __init__(self, ip: str = '0') -> None:
        self.db = Mongo()
        self.many = False

        if ip != '0':
            self.ip = ip
            self._strategy = Switch(self.ip)
            self.device = self.db.select_device(ip)
            try:
                self.vendor = self.device['vendor']
                self.community = self.device['community']
                self.snmp_version = self.device['snmp_version']
                self.model = self.device['model']
                self.status = self.device['online']
                self.vendor_switch()
            except TypeError:
                print('Equipamento não encontrado')
                return None
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

    def lldp(self, ip):
        if self.many:
            print("Atualizando o LLDP de todos os Switches huawei")
            device = self.db.select_device(ip)
            ip = device['ip']
            name = device['name']
            status = device['online']
            disable = device['disable_st']
            vendor = device['vendor']
            test = False
            print(f"Switch {name}")

            if vendor == 'Huawei':
                test = True

            if status == '1' and disable == '0' and test:
                try:
                    lldp = LldpSwitch(ip)
                    lldp._strategy.set_lldp()
                except:
                    pass
        else:
            try:
                device = self.db.select_device(self.ip)
                status = device['online']
                disable = device['disable_st']
            except TypeError:
                return 0
            if status == '1' and disable == '0':
                lldp = LldpSwitch(self.ip)
                lldp._strategy.set_lldp()
                print("#" * 20)

    def lldp_conf(self):
        if self.many:
            ip_list = self.ip_list()
            try:
                create_threads_bkp(ip_list, self.lldp)

            except KeyboardInterrupt:
                print("Cancelado pelo Administrador")

        else:
            try:
                self.lldp(self.ip)
            except KeyboardInterrupt:
                print("Cancelado pelo Administrador")
                return False
            except FileNotFoundError:
                print("Arquivo de LOG não encontrado")
                return False
            except:
                print("Erro! Tratar no arquivo backup_st_configurations_thread.py")
                return False


if __name__ == "__main__":
    # net = NetworkTools()
    # net.status_all_devices()
    scan = LldpSwitch()
    scan.lldp()
