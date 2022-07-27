from colorama import Fore
from .mongodb.mongo_device import Mongo
from .mongodb.mongo_reports import Mongo as MongoReports
from .layer7.snmp_functions import SnmpFunctions
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
from .switches.tools import ToolsSwitch as toolsSt
from .switches.vendor.hp import Hp


class Scanner:

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

    def scan_switch(self):
        if self.many:
            print("Escaneando todos os Switches")
            devices = self.db.select_all_devices()
            for device in devices:
                status = device['online']
                disable = device['disable_st']
                disable_scan = device['disable_scan']



                """date_backup = device['last_backup']                             
                from datetime import datetime
                data_e_hora_atuais = datetime.now()
                data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y')

                print(data_e_hora_em_texto)
                print(date_backup)"""

                if status == '1' and disable == '0' and disable_scan == '0':
                    vendor = device['vendor']
                    community = device['community']
                    snmp_version = device['snmp_version']
                    model = device['model']
                    location = device['location']
                    patrimony = device['patrimony']
                    ip = device['ip']
                    new_community = community
                    # tenta conectar via snmp
                    snmp = SnmpFunctions(ip, community, snmp_version)
                    try:
                        info_switch = snmp.snmp_info_switch()
                        if info_switch is None:
                            # nesse caso tenta outras comunidades snmp
                            new_community = snmp.community_discovery()
                    except:
                        # testa verifica a comunidade e tenta novamente
                        new_community = snmp.community_discovery()

                    try:
                        snmp = SnmpFunctions(ip, new_community, snmp_version)
                        info_switch = snmp.snmp_info_switch()
                    except:
                        print(f"Algo errado não está certo. Verifique o switch: {ip}")
                        print("####################")
                        continue
                    # testa se os dados atuais, são diferentes dos buscados via snmp
                    try:

                        snmp_vendor = info_switch['vendor']
                        snmp_model = info_switch['model']
                        snmp_location = info_switch['location']
                        snmp_patrimony = info_switch['patrimony']
                        mac = device['mac']

                        if mac == 'NaN' or mac == 'None' or mac == '' or mac == '-' or mac == '0':
                            _strategy = Switch(ip)
                            try:
                                mac_new = _strategy.get_mac_switch_by_snmp()
                                self.db.update_device({'ip': ip}, {'mac': mac_new})
                                print(Fore.RED + mac_new + Fore.RESET)
                            except TypeError:
                                print('Deu ruim na busca de Mac por SNMP')
                        else:
                            print(mac)

                        if snmp_vendor != vendor:
                            try:
                                self.db.update_device({'ip': ip}, {'vendor': snmp_vendor})
                                print(Fore.RED + snmp_vendor + Fore.RESET)
                            except TypeError:
                                print("interrompido pelo ADM")
                        else:
                            print(snmp_vendor)

                        if snmp_model != model:
                            try:
                                self.db.update_device({'ip': ip}, {'model': snmp_model})
                                print(Fore.RED + snmp_model + Fore.RESET)
                            except TypeError:
                                print("interrompido pelo ADM")
                        else:
                            print(snmp_model)

                        if snmp_location != location:
                            try:
                                self.db.update_device({'ip': ip}, {'location': snmp_location})
                                print(Fore.RED + snmp_location + Fore.RESET)
                            except TypeError:
                                print("interrompido pelo ADM")
                        elif snmp_location == '':
                            try:
                                self.db.update_device({'ip': ip}, {'location': 'NaN'})
                            except TypeError:
                                print("interrompido pelo ADM")
                        else:
                            print(snmp_location)

                        if snmp_patrimony != patrimony:
                            try:
                                self.db.update_device({'ip': ip}, {'patrimony': snmp_patrimony})
                                print(Fore.RED + snmp_patrimony + Fore.RESET)
                            except TypeError:
                                print("interrompido pelo ADM")
                        else:
                            print(snmp_patrimony)

                        print("#" * 20)
                    except  KeyboardInterrupt:
                        print("interrompido pelo ADM")
                    except TypeError:
                        pass
            # adiciona em reports o último scan completo
            mongoRep = MongoReports()
            mongoRep.update_date_last_scan()
        else:
            try:
                device = self.db.select_device(self.ip)
                status = device['online']
                disable = device['disable_st']
                disable_scan = device['disable_scan']

            except TypeError:
                return 0

            print(f'Status:{status} disable={disable} disable_scan={disable_scan}')
            if status == '1' and disable == '0' and disable_scan == '0':
                vendor = device['vendor']
                community = device['community']
                snmp_version = device['snmp_version']
                model = device['model']
                location = device['location']
                patrimony = device['patrimony']
                ip = device['ip']
                mac = device['mac']

                new_community = self.community
                # tenta conectar via snmp
                # tenta conectar via snmp
                snmp = SnmpFunctions(ip, community, snmp_version)
                try:
                    info_switch = snmp.snmp_info_switch()
                    if info_switch is None:
                        # nesse caso tenta outras comunidades snmp
                        new_community = snmp.community_discovery()
                except:
                    # testa verifica a comunidade e tenta novamente
                    new_community = snmp.community_discovery()

                try:
                    mac_new = self._strategy.get_mac_switch_by_snmp()
                    self.db.update_device({'ip': ip}, {'mac': mac_new})
                    print(mac_new)
                except TypeError:
                    print('Deu ruim na busca de Mac por SNMP')


                try:
                    snmp = SnmpFunctions(ip, new_community, snmp_version)
                    info_switch = snmp.snmp_info_switch()
                except:
                    print(f"Não conseguiu identificar a comunidade SNMP do switch: {ip}")
                    pass
                # testa se os dados atuais, são diferentes dos buscados via snmp
                try:
                    snmp_vendor = info_switch['vendor']
                    snmp_model = info_switch['model']
                    snmp_location = info_switch['location']
                    snmp_patrimony = info_switch['patrimony']

                    if snmp_vendor != vendor:
                        try:
                            self.db.update_device({'ip': ip}, {'vendor': snmp_vendor})
                            print(Fore.RED + snmp_vendor + Fore.RESET)
                        except TypeError:
                            print("interrompido pelo ADM")
                    else:
                        print(snmp_vendor)

                    if snmp_model != model:
                        try:
                            self.db.update_device({'ip': ip}, {'model': snmp_model})
                            print(Fore.RED + snmp_model + Fore.RESET)
                        except TypeError:
                            print("interrompido pelo ADM")
                    else:
                        print(snmp_model)

                    if snmp_location != location and snmp_location != '':
                        try:
                            self.db.update_device({'ip': ip}, {'location': snmp_location})
                            print(Fore.RED + snmp_location + Fore.RESET)
                        except TypeError:
                            print("interrompido pelo ADM")
                    elif snmp_location == '':
                        try:
                            self.db.update_device({'ip': ip}, {'location': 'NaN'})
                        except TypeError:
                            print("interrompido pelo ADM")
                    else:
                        print(snmp_location)

                    if snmp_patrimony != patrimony:
                        try:
                            self.db.update_device({'ip': ip}, {'patrimony': snmp_patrimony})
                            print(Fore.RED + snmp_patrimony + Fore.RESET)
                        except TypeError:
                            print("interrompido pelo ADM")
                    else:
                        print(snmp_patrimony)

                    print("#" * 20)
                except  KeyboardInterrupt:
                    print("interrompido pelo ADM")
                except TypeError:
                    pass

                print("#" * 20)

    def get_template_switch(self):
        devices = self.db.select_all_devices()
        for device in devices:
            vendor = device['vendor']
            model = device['model']
            ip = device['ip']
            status = device['online']

            # a partir daqui, apenas se tiver online
            if status == '1':
                # Quantidade de portas
                ports = toolsSt.number_of_ports(vendor, model)

                # atualiza no banco
                if ports != 0:
                    self.db.update_device({'ip': ip}, {'ports_mac': ports})

    def scan_fdb(self):
        if self.many:
            devices = self.db.select_all_devices()
            for device in devices:
                ip = device['ip']
                print(f'Switch: {ip}')
                status = device['online']
                scan = Scanner(ip)
                disable = device['disable_st']

                if status == '0' and disable == '0':
                    print(f"O switch {ip}, está Offline")
                else:
                    response = scan._strategy.get_mac_table()
                    print(response)
                    self.db.update_device({'ip': ip}, {'ports_mac': response})
        else:
            if self.status == '0':
                print(f'Switch {self.ip} Offline')
            else:
                print(f'Buscando Switch {self.ip}')
                response = self._strategy.get_mac_table()
                self.db.update_device({'ip': self.ip}, {'ports_mac': response})

    def scan_ports(self):
        devices = self.db.select_all_devices()
        for device in devices:
            ip = device['ip']
            vendor = device['vendor']
            model = device['model']
            ports = toolsSt.format_port('0', vendor, model)
            if model == 'NaN' or vendor == 'NaN':
                print(f"Switch {ip}: não foi informado o Fabricante e/ou modelo do equipamento")

            all_ports = ''
            for port in ports:
                all_ports += port + ','
            all_ports = all_ports[:-1]
            self.db.update_device({'ip': ip}, {'ports': all_ports})

    """def scan_ports_map(self):
        devices = self.db.select_all_devices()
        for device in devices:
            sysname = device['name'].split('.')[0]
            hostname = device['name']
            manually: "1"
            vendor = device['vendor']
            model = device['model']

            ports = toolsSt.format_port('0', vendor, model)
            all_ports = ''
            for port in ports:
                all_ports += port + ','
            all_ports = all_ports[:-1]
            self.db.update_device({'ip': ip}, {'ports': all_ports})
    """

    def popular_novo_campo(self):
        devices = self.db.select_all_devices()
        for device in devices:
            ip = device['ip']
            print(ip)
            self.db.update_device({'ip': ip}, {'last_backup': 'NaN'})


if __name__ == "__main__":
    # net = NetworkTools()
    # net.status_all_devices()
    scan = Scanner()
    scan.scan_switch()
