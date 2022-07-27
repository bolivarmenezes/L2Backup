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


class NtpSwitch:

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

    def ntp_server(self):
        if self.many:
            print("Atualizando o NTP de todos os Switches")
            devices = self.db.select_all_devices()
            test2 = False
            for device in devices:
                ip = device['ip']
                print(f"Tentando {ip}")
                status = device['online']
                disable = device['disable_st']
                vendor = device['vendor']
                test = False

                '''if vendor == 'Aruba':
                    test = True

                if ip == "192.168.19.52":
                    test2 = True
                
                if status == '1' and disable == '0' and test and test2:'''
                if status == '1' and disable == '0':
                    ntp = NtpSwitch(ip)
                    ntp._strategy.set_ntp()
        else:
            try:
                device = self.db.select_device(self.ip)
                status = device['online']
                disable = device['disable_st']
            except TypeError:
                return 0
            if status == '1' and disable == '0':
                ntp = NtpSwitch(self.ip)
                ntp._strategy.set_ntp()
                print("#" * 20)



if __name__ == "__main__":
    # net = NetworkTools()
    # net.status_all_devices()
    scan = NtpSwitch()
    scan.ntp_server()
