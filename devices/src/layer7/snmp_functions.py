from datetime import timedelta
from re import search, IGNORECASE
from colorama import Fore
from easysnmp import Session
from easysnmp import EasySNMPTimeoutError
from devices.src.mongodb.mongo_device import Mongo


class SnmpFunctions:

    def __init__(self, hostname, community='public', version=2, sprint_value=False):
        self.hostname = hostname
        self.community = community
        self.version = version
        try:
            self.session = Session(hostname=self.hostname, community=self.community, version=self.version,
                                   use_sprint_value=sprint_value)
        except EasySNMPTimeoutError:
            print("Time out: verifique a disponibilidade do dispositivo")

    def snmp_get(self, command='sysUpTime.0'):
        try:
            response = self.session.get(command).value
        except SystemError:
            # Comunidade incorreta
            response = None
        return response

    def snmp_set(self, command, value):
        self.session.set(command, value)

    def snmp_walk(self, command):
        try:
            resp = self.session.walk(command)
        except EasySNMPTimeoutError:
            # tenta de novo. Se não der, deixa pra la :D
            try:
                resp = self.session.walk(command)
            except EasySNMPTimeoutError:
                print("Timeout na função snmp_walk\nComo diria o kiko: NÃO DEU!")
        except SystemError:
            print("Algo errado não está certo. Verifique a comunicação com o dispositivo")
        return resp

    def community_discovery(self):
        community_list = ['public', 'public2', 'public3', 'public4']
        versions = [2, 1]

        for version in versions:
            for community in community_list:
                # print(f'Testando: {community}')
                print(self.hostname, community, version)
                try:
                    session_test = SnmpFunctions(
                        hostname=self.hostname, community=community, version=version)
                    session_test.session.get('sysUpTime.0')

                    # uma vez encontrada, a comunidade correta é atualizada na base de dados
                    db = Mongo()
                    db.update_device({"ip": self.hostname}, {
                                     "community": community})
                    if version == 1:
                        db.update_device({"ip": self.hostname}, {
                                         "snmp_version": version})
                    print("Salvando...")
                    return community
                except:
                    pass
        return None

    def snmp_info_switch(self):
        # testa se a comunidade está correta
        try:
            location = self.snmp_get("sysLocation.0")
            if location is None:
                return None
            vendor_aux = self.snmp_get("sysDescr.0")
            uptime = self.snmp_get("sysUpTimeInstance")
            patrimony = self.snmp_get("sysContact.0")
        except:
            return None
        # convert para tipo tempo, e para string, para excluir os milisegundos
        try:
            seconds = int(uptime) / 100
            up_time = timedelta(seconds=seconds)
            up_time = str(up_time).split(".")[0]
        except TypeError:
            pass
        # para uniformizar os nomes
        try:
            vendor = self.parser_vendor(vendor_aux)
            model = self.parser_model(vendor_aux)
            response = {
                'vendor': vendor,
                'model': model,
                'patrimony': patrimony,
                'location': location,
                'uptime': up_time
            }

            return response

        except TypeError:
            print(Fore.RED + "Busca interrompida pelo administrador" + Fore.RESET)

    @staticmethod
    def parser_vendor(data):
        if search('\\bd-link\\b', data, IGNORECASE):
            vendor = "D-Link"
        elif search('Aruba', data, IGNORECASE):
            vendor = "Aruba"
        elif search('2530-24G', data, IGNORECASE):
            vendor = "Aruba"
        elif search('2530-48G', data, IGNORECASE):
            vendor = "Aruba"
        elif search('\\bDES\\b', data, IGNORECASE):
            vendor = "D-Link"
        elif search('\\bTigerSwitch\\b', data, IGNORECASE):
            vendor = "SMC"
        elif search('\\bSGX3226\\b', data, IGNORECASE):
            vendor = "Planet"
        elif search('\\bHP\\b', data, IGNORECASE):
            vendor = "HP"
        elif search('\\bSG300\\b', data, IGNORECASE):
            vendor = "Cisco"
        elif search('\\bHuawei\\b', data, IGNORECASE):
            vendor = "Huawei"
        elif search('\\b1920-24G\\b', data, IGNORECASE):
            vendor = "HP"
        elif search('\\bDell\\b', data, IGNORECASE):
            vendor = "Dell"
        elif search('\\bHewlett\\b', data, IGNORECASE):
            vendor = "HP"
        elif search('\\b10/100\\b', data, IGNORECASE):
            vendor = "Cisco"
        elif search('\\bExtremeXOS\\b', data, IGNORECASE):
            vendor = "ExtremeXOS"
        elif search('\\bBaseline\\b', data, IGNORECASE):
            vendor = "3com"
        elif search('\\bDGS\\b', data, IGNORECASE):
            vendor = "D-Link"
        elif search('\\bPLANET\\b', data, IGNORECASE):
            vendor = "Planet"
        elif search('\\bECS2000-26T\\b', data, IGNORECASE):
            vendor = "Edge-Core"
        elif search('\\bFast Ethernet Switch\\b', data, IGNORECASE):
            vendor = "D-Link"
        elif search('\\bJetStream\\b', data, IGNORECASE):
            vendor = "TP-Link"
        elif search('24-Port 10/100Mbps', data, IGNORECASE):
            vendor = "TP-Link"
        elif search('HP V1910-24G', data, IGNORECASE):
            vendor = "HP"
        elif search('\\bSF300\\b', data, IGNORECASE):
            vendor = "Cisco"

        else:
            vendor = data

        return vendor

    @staticmethod
    def parser_model(data):
        if search('\\bDES-3028\\b', data, IGNORECASE):
            model = "DES-3028"
        elif search('\\bDES-3200\\b', data, IGNORECASE):
            model = "DES-3200"
        elif search('\\bSMC6128L2\\b', data, IGNORECASE):
            model = "SMC6128L2"
        elif search('\\bSMC6152L2\\b', data, IGNORECASE):
            model = "SMC6152L2"
        elif search('\\bDES-3226L\\b', data, IGNORECASE):
            model = "DES-3226L"
        elif search('\\bDES-3052\\b', data, IGNORECASE):
            model = "DES-3052"
        elif search('\\bDES-3526\\b', data, IGNORECASE):
            model = "DES-3526"
        elif search('\\bSGX3226\\b', data, IGNORECASE):
            model = "SGX3226"
        elif search('\\bSF300-24\\b', data, IGNORECASE):
            model = "SF300-24"
        elif search('\\bSF300-48\\b', data, IGNORECASE):
            model = "SF300-48"
        elif search('\\bDES-1210-28\\b', data, IGNORECASE):
            model = "DES-1210-28"
        elif search('\\b2530-24G\\b', data, IGNORECASE):
            model = "2530-24G"
        elif search('\\b10/100\\b', data, IGNORECASE):
            model = "SF300-24"
        elif search('\\bS5720-28X-LI-AC\\b', data, IGNORECASE):
            model = "S5720-28X-LI-AC"
        elif search('\\bS5720-52X-PWR-LI-AC\\b', data, IGNORECASE):
            model = "S5720-52X-PWR-LI-AC"
        elif search('\\bS5735-L48T4X-A1\\b', data, IGNORECASE):
            model = "S5735-L48T4X-A1"
        elif search('\\b1920-24G\\b', data, IGNORECASE):
            model = "1920-24G"
        elif search('\\bN1524\\b', data, IGNORECASE):
            model = "N1524"
        elif search('\\b1920-48G\\b', data, IGNORECASE):
            model = "1920-48G"
        elif search('\\bDES-3528\\b', data, IGNORECASE):
            model = "DES-3528"
        elif search('\\bSG300-28PP\\b', data, IGNORECASE):
            model = "SG300-28PP"
        elif search('\\b2530-48G\\b', data, IGNORECASE):
            model = "2530-48G"
        elif search('\\bX450e-48p\\b', data, IGNORECASE):
            model = "X450e-48p"
        elif search('\\bS5720-52X-LI-AC\\b', data, IGNORECASE):
            model = "S5720-52X-LI-AC"
        elif search('\\bS5720-28X-PWR-LI-AC\\b', data, IGNORECASE):
            model = "S5720-28X-PWR-LI-AC"
        elif search('\\bDES-3550\\b', data, IGNORECASE):
            model = "DES-3550"
        elif search('\\b2226-SFP\\b', data, IGNORECASE):
            model = "2226-SFP"
        elif search('\\DGS-3224TGR\\b', data, IGNORECASE):
            model = "DGS-3224TGR"
        elif search('\\bSGSW-2402\\b', data, IGNORECASE):
            model = "SGSW-2402"
        elif search('\\bDGS-3324SRi\\b', data, IGNORECASE):
            model = "DGS-3324SRi"
        elif search('\\bECS2000-26T\\b', data, IGNORECASE):
            model = "ECS2000-26T"
        elif search('\\bDES-3028P\\b', data, IGNORECASE):
            model = "DES-3028P"
        elif search('\\bFast Ethernet Switch\\b', data, IGNORECASE):
            model = "DES-3250TG"
        elif search('\\bDES-3250TG\\b', data, IGNORECASE):
            model = "DES-3250TG"
        elif search('\\bX450a-24t\\b', data, IGNORECASE):
            model = "X450a-24t"
        elif search('\\bX460G2-24x-10G4\\b', data, IGNORECASE):
            model = "X460G2-24x-10G4"
        elif search('\\bv1251b6\\b', data, IGNORECASE):
            model = "X450e-48p"
        elif search('\\bX670-48x\\b', data, IGNORECASE):
            model = "X670-48x"
        elif search('\\bJetStream\\b', data, IGNORECASE):
            model = "JetStream"
        elif search('\\b24-Port 10/100Mbps\\b', data, IGNORECASE):
            model = "tplink"
        elif search('\\b2250-SFP\\b', data, IGNORECASE):
            model = "2250-SFP"
        elif search('\\bV1910-24G\\b', data, IGNORECASE):
            model = "V1910-24G"
        elif search('\\bV1905-48\\b', data, IGNORECASE):
            model = "V1905-48"
        elif search('\\b2930F-48G-4SFP+\\b', data, IGNORECASE):
            model = "2930F-48G-4SFP+"
        else:
            model = data
        return model


if __name__ == "__main__":
    snmp = SnmpFunctions("127.0.0.1", "public")
    retur = snmp.snmp_get('sysName.0')
    print(retur)
