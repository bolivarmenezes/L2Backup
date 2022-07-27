from devices.src.manager_files.manager_date_file import ManagerDateBackups
from devices.src.mongodb.mongo_device import Mongo
from devices.src.mongodb.mongo_reports import Mongo as mongo_reports
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
from datetime import datetime
from devices.src.layer7.create_threads_bkp import create_threads_bkp


class BackupSt:

    def __init__(self, ip: str = '0') -> None:
        self.db = Mongo()
        self.many = False

        if ip != '0':
            # se entrar aqui, significa que o IP foi passado
            self.ip = ip
            self._strategy = Switch(self.ip)
            self.device = self.db.select_device(ip)
            self.vendor = self.device['vendor']
            self.community = self.device['community']
            self.snmp_version = self.device['snmp_version']
            self.model = self.device['model']
            try:
                self.status = self.device['online']
            except KeyError:
                self.status = '1'
                self.db.update_device({'ip': ip}, {'online': '1'})
            self.vendor_switch()
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
        date = datetime.now()
        date_today = date.strftime('%d/%m/%Y %H:%M')
        for device in devices:
            last_bkp = device['last_backup'].split(' ')[0]
            current_date = date_today.split(' ')[0]
            disable = device['disable_st']
            status = device['online']
            test_date = True
            disable_scan = device['disable_scan']
            enable_scan = False
            if disable_scan == '0':
                enable_scan = True
            '''
            Apenas faz backup se já não tiver feito no dia
            '''
            if last_bkp == current_date:
                test_date = False
            else:
                print(f'Data Atual: {current_date}, Data do último Backup: {last_bkp}')

            '''
            Parte de testes
            test_vendor = False
            vendor = device['vendor']
            if vendor == 'Huawei':
                test_vendor = True
            if disable == '0' and status == '1' and test_vendor and enable_scan:'''

            if disable == '0' and status == '1' and test_date and enable_scan:
                ip_list.append(device['ip'])
        return ip_list

    def backup(self, ip):
        device = self.db.select_device(ip)
        name = device['name']
        bkp = BackupSt(ip)
        status_bkp = bkp._strategy.backup_configuration()
        if status_bkp:
            # atualiza data do backup
            mb = ManagerDateBackups(name)
            mb.manager_date()
            self.db.update_device(
                {'ip': ip}, {'last_backup_error': '0'})

        else:
            date = datetime.now()
            date_bkp = date.strftime('%d/%m/%Y %H:%M')
            self.db.update_device(
                {'ip': ip}, {'last_backup_error': date_bkp})

    def backup_conf(self):
        if self.many:
            ip_list = self.ip_list()
            try:
                create_threads_bkp(ip_list, self.backup)
                """ adicionar data do último backup completo """
                m_report = mongo_reports()
                m_report.update_date_last_backup()

            except KeyboardInterrupt:
                print("Cancelado pelo Administrador")

        else:
            try:
                self.backup(self.ip)
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
    backup = BackupSt('192.168.8.32')
    backup.backup_conf()
