import abc
import re
from devices.src.mongodb.mongo_device import Mongo
from devices.src.switches.vendor.switch_base import SwitchBase
from devices.src.layer7.snmp_functions import SnmpFunctions
from datetime import datetime
import devices.database.path_of_files as path_pass

"""
Switch é uma classe abstrata, que chama as respectivas 
classes concretas (conforme o fabricante/modelo)
"""


class Switch(abc.ABC):
    def __init__(self, ip: str) -> None:
        self.ip = ip
        try:
            # para acesso snmp
            self.community = self.get_community()
            self.version = self.get_snmp_version()
            self.model = self.get_model()
            self.snmp = SnmpFunctions(self.ip, self.community, self.version)
        except KeyboardInterrupt:
            print("Cancelado pelo administrador")
        except TypeError:
            pass

    def get_tftp_server(self):
        host_test = self.ip.split(
            '.')[0] + '.' + self.ip.split('.')[1] + '.' + self.ip.split('.')[2]
        if host_test == '192.168.35':
            return path_pass.tftp_server_private
        else:
            return path_pass.tftp_server

    def get_device_by_ip(self):
        db = Mongo()
        return db.select_device(self.ip)

    def update_device(filter_search: dict, **kwargs) -> None:
        """
        :param filter_search: (dict) campo que será utilizado para filtrar a busca
        :param kwargs: (dict) chave:valor (campo:novo_dado) que devem ser atualizados
        """
        db = Mongo()
        for k in kwargs.keys():
            db.update_device(filter_search, {k: kwargs[k]})

    def get_community(self) -> str:
        try:
            switch_base = SwitchBase(self.ip)
        except TypeError:
            return '0'
        return switch_base.get_community

    def get_patrimony(self) -> str:
        try:
            switch_base = SwitchBase(self.ip)
        except TypeError:
            return '0'
        return switch_base.get_patrimony

    def get_location(self) -> str:
        try:
            switch_base = SwitchBase(self.ip)
        except TypeError:
            return '0'
        return switch_base.get_location

    def get_snmp_version(self) -> str:
        try:
            switch_base = SwitchBase(self.ip)
        except TypeError:
            return '0'
        return switch_base.get_snmp_version

    def get_model(self) -> str:
        try:
            switch_base = SwitchBase(self.ip)
        except TypeError:
            return '0'
        return switch_base.get_model

    def get_vendor(self) -> str:
        try:
            switch_base = SwitchBase(self.ip)
        except TypeError:
            return '0'
        return switch_base.get_vendor

    def get_patrimony_by_snmp(self) -> str:
        switch_base = SwitchBase(self.ip)
        return switch_base.get_patrimony_by_snmp

    def get_location_by_snmp(self) -> str:
        switch_base = SwitchBase(self.ip)
        return switch_base.get_location_by_snmp

    def get_vendor_by_snmp(self) -> str:
        switch_base = SwitchBase(self.ip)
        return switch_base.get_vendor_by_snmp

    def get_uptime_by_snmp(self) -> str:
        switch_base = SwitchBase(self.ip)
        return switch_base.get_uptime_by_snmp

    def get_lldp_by_snmp(self):
        pass

    def get_mac_switch_by_snmp(self):
        switch_base = SwitchBase(self.ip)
        return switch_base.get_mac_switch_by_snmp()

    def get_mac_table(self):
        switch_base = SwitchBase(self.ip)
        return switch_base.get_mac_table()

    def get_interfaces_by_snmp(self):
        pass

    def get_vlan_by_snmp(self):
        pass

    def get_ports_mac(self):
        pass

    def get_name(self):
        switch_base = SwitchBase(self.ip)
        return switch_base.get_name

    def get_sysname(self):
        switch_base = SwitchBase(self.ip)
        return switch_base.get_sysname

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

    def backup_configuration(self) -> bool:
        '''
         Return true (for bkp ok) or false (for failure)
        '''
        switch_base = SwitchBase(self.ip)
        return switch_base.backup_configuration()

    # def save_bkp(self):
    #    pass

    def create_template_st(self):
        switch_base = SwitchBase(self.ip)

    def get_neighbour(self):
        switch_base = SwitchBase(self.ip)
        return switch_base.get_neighbour()

    def set_ntp(self):
        switch_base = SwitchBase(self.ip)
        return switch_base.set_ntp()

    def set_lldp(self):
        switch_base = SwitchBase(self.ip)
        return switch_base.set_lldp()

    def name_bkp(self, name: str, vendor: str, model: str):
        date = datetime.now()
        # name_bkp = name + '_' + date.strftime('%Y-%m-%d') + '_' + vendor + '_' + model + '.cfg'
        print(f"Marca: {vendor} Modelo:{model}")
        if '-' in vendor:
            vendor = vendor.replace('-', '')
        # name_bkp = name + '-' + vendor+'.cfg'
        # name_bkp = name + '_' + date.strftime('%Y-%m-%d') + '_' + vendor + '_' + model + '.cfg'
        name_bkp = name + '_' + vendor + '_' + model + '.cfg'
        return name_bkp
