"""
Gerencia o mongo db
"""
from datetime import datetime
from pymongo import MongoClient
from pymongo import errors


class Mongo:

    def __init__(self):
        """
            Conectando no bando de dados
            criando (se não existe) ou acessando o banco de dados
        """
        try:
            self.client = MongoClient("localhost", 27017)
            self.database = self.client['Devices']
        except:
            print('Erro ao conectar no MongoDB')

    def insert_device(self, device: dict) -> None:
        """
        :param device: dicionário contendo os dados do dispositivo
        :return: retorno da operação de inserção
        """
        device['ap_last_modified'] = datetime.utcnow().today()
        try:
            if device is not None:
                self.database.devices_ap.insert_one(device)
                print("O dispositivo foi adicionado com sucesso")
            else:
                raise Exception(
                    "O dispositivo não foi adicionado, porque o parâmetro passado é None")
        except errors.DuplicateKeyError:
            print(f'O dispositivo já foi adicionado anteriormente')

    def insert_many_devices(self, devices) -> None:
        try:
            if devices is not None:
                self.database.devices_ap.insert_many(devices)
                print("Os dispositivos foram adicionados com sucesso")
            else:
                raise Exception(
                    "Os dispositivos não foram adicionados, porque o parâmetro passado é None")
        except errors.DuplicateKeyError:
            print(f'O(s) dispositivos já consta(m) na base de dados')

    def select_device(self, ip):
        """
        :param ip: ip
        :return: retorna um dicionário
        """
        return self.database.devices_ap.find_one({"ap_ip": ip})

    def select_device_field_by_ip(self, ip: str, field: str):
        return self.database.devices_ap.find_one({"ap_ip": ip}, {field})

    def select_all_devices(self):
        devices = self.database.devices_ap.find()
        at_least_one_item = False
        list_of_devices: list = []
        for device in devices:
            at_least_one_item = True
            list_of_devices.append(device)
        if not at_least_one_item:
            return "A base de dados está vazia"
        return list_of_devices

    def update_device(self, filter: dict, data: dict):
        self.database.devices_ap.update_one(filter, {'$set': data})

    def delete_device(self, ip) -> None:
        self.database.devices_ap.delete_one({"ap_ip": ip})

    def delete_field(self, ip: dict, name_field: dict):
        self.database.devices_ap.update_one(ip, {'$unset': name_field})


if __name__ == "__main__":
    db = Mongo()
    db.insert_device({"ap_hostname": "ap-228355.wifi.ufsm.br", "ap_sysname": "ap-228355", "ap_ip": "192.168.28.148",
                      "ap_mac": "3C:08:F6:47:1E:46", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO F 2º Andar", "ap_patrimony": "228355", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228356.wifi.ufsm.br", "ap_sysname": "ap-228356", "ap_ip": "192.168.28.147",
                      "ap_mac": "3C:08:F6:47:1E:40", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO F 2º Andar", "ap_patrimony": "228356", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228357.wifi.ufsm.br", "ap_sysname": "ap-228357", "ap_ip": "192.168.28.146",
                      "ap_mac": "3C:08:F6:47:1E:44", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO F 2º Andar", "ap_patrimony": "228357", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228358.wifi.ufsm.br", "ap_sysname": "ap-228358", "ap_ip": "192.168.28.145",
                      "ap_mac": "00:22:BD:FE:56:F7", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO F 2º Andar", "ap_patrimony": "228358", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228359.wifi.ufsm.br", "ap_sysname": "ap-228359", "ap_ip": "192.168.28.144",
                      "ap_mac": "D0:72:DC:09:04:6F", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO F 2º Andar", "ap_patrimony": "228359", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-235901.wifi.ufsm.br", "ap_sysname": "ap-235901", "ap_ip": "192.168.28.195",
                      "ap_mac": "88:F0:31:9A:FB:81", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO F 2º Andar", "ap_patrimony": "235901", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-235902.wifi.ufsm.br", "ap_sysname": "ap-235902", "ap_ip": "192.168.28.149",
                      "ap_mac": "88:F0:31:9A:FB:B7", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO F 2º Andar", "ap_patrimony": "235902", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231051.wifi.ufsm.br", "ap_sysname": "ap-231051", "ap_ip": "192.168.28.151",
                      "ap_mac": "88:F0:31:80:D9:BC", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO B", "ap_patrimony": "231051", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228323.wifi.ufsm.br", "ap_sysname": "ap-228323", "ap_ip": "192.168.28.216",
                      "ap_mac": "D0:72:DC:09:04:C6", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO D", "ap_patrimony": "228323", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228324.wifi.ufsm.br", "ap_sysname": "ap-228324", "ap_ip": "192.168.28.217",
                      "ap_mac": "D0:72:DC:09:04:C4", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO D", "ap_patrimony": "228324", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228325.wifi.ufsm.br", "ap_sysname": "ap-228325", "ap_ip": "192.168.28.218",
                      "ap_mac": "3C:08:F6:47:1E:66", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO D", "ap_patrimony": "228325", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228326.wifi.ufsm.br", "ap_sysname": "ap-228326", "ap_ip": "192.168.28.219",
                      "ap_mac": "3C:08:F6:47:1E:91", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO D", "ap_patrimony": "228326", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228327.wifi.ufsm.br", "ap_sysname": "ap-228327", "ap_ip": "192.168.28.220",
                      "ap_mac": "3C:08:F6:47:1E:3F", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO D", "ap_patrimony": "228327", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-235905.wifi.ufsm.br", "ap_sysname": "ap-235905", "ap_ip": "192.168.28.250",
                      "ap_mac": "F8:C2:88:B4:F0:1E", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO A", "ap_patrimony": "235905", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231046.wifi.ufsm.br", "ap_sysname": "ap-231046", "ap_ip": "192.168.28.48",
                      "ap_mac": "88:F0:31:8C:0A:56", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO A", "ap_patrimony": "231046", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231045.wifi.ufsm.br", "ap_sysname": "ap-231045", "ap_ip": "192.168.28.47",
                      "ap_mac": "88:F0:31:8C:0A:3C", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO A", "ap_patrimony": "231045", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231047.wifi.ufsm.br", "ap_sysname": "ap-231047", "ap_ip": "192.168.28.49",
                      "ap_mac": "88:F0:31:80:D9:E1", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO A", "ap_patrimony": "231047", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231044.wifi.ufsm.br", "ap_sysname": "ap-231044", "ap_ip": "192.168.28.46",
                      "ap_mac": "88:F0:31:80:D9:CC", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO C", "ap_patrimony": "231044", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231043.wifi.ufsm.br", "ap_sysname": "ap-231043", "ap_ip": "192.168.28.45",
                      "ap_mac": "88:F0:31:80:D9:FC", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "POLITEC - BLOCO C", "ap_patrimony": "231043", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237429.wifi.ufsm.br", "ap_sysname": "ap-237429", "ap_ip": "192.168.28.158",
                      "ap_mac": "F4:CF:E2:2E:6C:6F", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - SALA 218 (Auditório)", "ap_patrimony": "237429", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228342.wifi.ufsm.br", "ap_sysname": "ap-228342", "ap_ip": "192.168.28.230",
                      "ap_mac": "00:22:BD:FE:56:FF", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 1º andar - Hall", "ap_patrimony": "228342", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237406.wifi.ufsm.br", "ap_sysname": "ap-237406", "ap_ip": "192.168.28.238",
                      "ap_mac": "F4:CF:E2:1C:63:E4", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 3º andar - próximo sala 321", "ap_patrimony": "237406",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228362.wifi.ufsm.br", "ap_sysname": "ap-228362", "ap_ip": "192.168.28.239",
                      "ap_mac": "D0:72:DC:09:04:C3", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 3º andar - próximo sala 351", "ap_patrimony": "228362",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237425.wifi.ufsm.br", "ap_sysname": "ap-237425", "ap_ip": "192.168.28.244",
                      "ap_mac": "F4:CF:E2:1C:63:79", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 2º andar - salão imembui", "ap_patrimony": "237425", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237426.wifi.ufsm.br", "ap_sysname": "ap-237426", "ap_ip": "192.168.28.205",
                      "ap_mac": "F4:CF:E2:B9:18:9F", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 1º andar corredor - SALA 130/133", "ap_patrimony": "237426",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237435.wifi.ufsm.br", "ap_sysname": "ap-237435", "ap_ip": "192.168.28.179",
                      "ap_mac": "F4:CF:E2:AC:29:CD", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 5º andar - Sala Reitor", "ap_patrimony": "237435", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237436.wifi.ufsm.br", "ap_sysname": "ap-237436", "ap_ip": "192.168.28.180",
                      "ap_mac": "F4:CF:E2:B9:18:EF", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 5º andar - Hall", "ap_patrimony": "237436", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237437.wifi.ufsm.br", "ap_sysname": "ap-237437", "ap_ip": "192.168.28.181",
                      "ap_mac": "F4:CF:E2:B9:18:F7", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 5º andar - Corredor LD", "ap_patrimony": "237437", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237421.wifi.ufsm.br", "ap_sysname": "ap-237421", "ap_ip": "192.168.28.240",
                      "ap_mac": "F4:CF:E2:B9:18:FE", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 6º andar - próximo sala 651", "ap_patrimony": "237421",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237422.wifi.ufsm.br", "ap_sysname": "ap-237422", "ap_ip": "192.168.28.241",
                      "ap_mac": "F4:CF:E2:D1:3A:7D", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 6º andar - próximo sala 619", "ap_patrimony": "237422",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237423.wifi.ufsm.br", "ap_sysname": "ap-237423", "ap_ip": "192.168.28.242",
                      "ap_mac": "F4:CF:E2:1C:63:4F", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 4º andar - próximo sala 415", "ap_patrimony": "237423",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237424.wifi.ufsm.br", "ap_sysname": "ap-237424", "ap_ip": "192.168.28.243",
                      "ap_mac": "F4:CF:E2:8D:3D:45", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 4º andar - próximo sala 436", "ap_patrimony": "237424",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237438.wifi.ufsm.br", "ap_sysname": "ap-237438", "ap_ip": "192.168.28.182",
                      "ap_mac": "F4:CF:E2:AC:29:AE", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 8º andar - Corredor LE", "ap_patrimony": "237438", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237439.wifi.ufsm.br", "ap_sysname": "ap-237439", "ap_ip": "192.168.28.183",
                      "ap_mac": "F4:CF:E2:B9:18:FC", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 8º andar - Corredor LD", "ap_patrimony": "237439", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237440.wifi.ufsm.br", "ap_sysname": "ap-237440", "ap_ip": "192.168.28.184",
                      "ap_mac": "F4:CF:E2:B9:18:21", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 9º andar - Sala Conselhos", "ap_patrimony": "237440",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237441.wifi.ufsm.br", "ap_sysname": "ap-237441", "ap_ip": "192.168.28.185",
                      "ap_mac": "F4:CF:E2:8D:3D:0E", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 9º andar - Corredor conselhos", "ap_patrimony": "237441",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237442.wifi.ufsm.br", "ap_sysname": "ap-237442", "ap_ip": "192.168.28.186",
                      "ap_mac": "F4:CF:E2:BE:C9:05", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 9º andar- corredor LD", "ap_patrimony": "237442", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228360.wifi.ufsm.br", "ap_sysname": "ap-228360", "ap_ip": "192.168.28.227",
                      "ap_mac": "3C:08:F6:47:1E:E3", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 7º andar - LE (PRPGP", "ap_patrimony": "228360", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228361.wifi.ufsm.br", "ap_sysname": "ap-228361", "ap_ip": "192.168.28.228",
                      "ap_mac": "D0:72:DC:1E:1B:8A", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "REITORIA - 7º andar - LD", "ap_patrimony": "228361", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237409.wifi.ufsm.br", "ap_sysname": "ap-237409", "ap_ip": "192.168.28.170",
                      "ap_mac": "F4:CF:E2:BE:C9:02", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "UNIÃO - RACK-2A-INF", "ap_patrimony": "237409", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237410.wifi.ufsm.br", "ap_sysname": "ap-237410", "ap_ip": "192.168.28.171",
                      "ap_mac": "F4:CF:E2:1C:63:D2", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "UNIÃO - RACK-2A-INF", "ap_patrimony": "237410", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-externo04.wifi.ufsm.br", "ap_sysname": "ap-externo04", "ap_ip": "192.168.28.83",
         "ap_mac": "34:DB:FD:DC:97:FC", "ap_model": "AIR-CAP1552E-N-K9", "ap_location": "PARQUE/ADM",
         "ap_patrimony": "226325", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-externo03.wifi.ufsm.br", "ap_sysname": "ap-externo03", "ap_ip": "192.168.28.82",
         "ap_mac": "34:DB:FD:DC:51:DC", "ap_model": "AIR-CAP1552E-N-K9", "ap_location": "AGITTEC",
         "ap_patrimony": "226321", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-externo02.wifi.ufsm.br", "ap_sysname": "ap-externo02", "ap_ip": "192.168.28.81",
         "ap_mac": "50:17:FF:DD:F9:7C", "ap_model": "AIR-CAP1552E-N-K9", "ap_location": "PARQUE/CPD",
         "ap_patrimony": "226322", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext-237447.wifi.ufsm.br", "ap_sysname": "ap-ext-237447", "ap_ip": "192.168.28.142",
         "ap_mac": "0C:F5:A4:96:CC:9C", "ap_model": "AIR-CAP1552E-N-K9", "ap_location": "Polivalente",
         "ap_patrimony": "237447", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-externo01.wifi.ufsm.br", "ap_sysname": "ap-externo01", "ap_ip": "192.168.28.80",
         "ap_mac": "50:17:FF:DD:F9:A0", "ap_model": "AIR-CAP1552E-N-K9", "ap_location": "Polivalente",
         "ap_patrimony": "0", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231029.wifi.ufsm.br", "ap_sysname": "ap-231029", "ap_ip": "192.168.28.104",
                      "ap_mac": "D0:72:DC:31:C0:B2", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "Polivalente",
                      "ap_patrimony": "231029", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231030.wifi.ufsm.br", "ap_sysname": "ap-231030", "ap_ip": "192.168.28.105",
                      "ap_mac": "D0:72:DC:31:C0:39", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "Polivalente",
                      "ap_patrimony": "231030", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231031.wifi.ufsm.br", "ap_sysname": "ap-231031", "ap_ip": "192.168.28.106",
                      "ap_mac": "D0:72:DC:1E:1B:9B", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "Polivalente",
                      "ap_patrimony": "231031", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231032.wifi.ufsm.br", "ap_sysname": "ap-231032", "ap_ip": "192.168.28.107",
                      "ap_mac": "80:E0:1D:A2:2D:55", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "Polivalente",
                      "ap_patrimony": "231032", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231036.wifi.ufsm.br", "ap_sysname": "ap-231036", "ap_ip": "192.168.28.111",
                      "ap_mac": "80:E0:1D:A2:2D:67", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "Polivalente",
                      "ap_patrimony": "231036", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231037.wifi.ufsm.br", "ap_sysname": "ap-231037", "ap_ip": "192.168.28.112",
                      "ap_mac": "80:E0:1D:A2:2D:5D", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "Polivalente",
                      "ap_patrimony": "231037", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224009.wifi.ufsm.br", "ap_sysname": "ap-224009", "ap_ip": "192.168.28.128",
                      "ap_mac": "C0:8C:60:29:98:67", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. principal: 1º Andar - Frente a SL 137", "ap_patrimony": "224009",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224010.wifi.ufsm.br", "ap_sysname": "ap-224010", "ap_ip": "192.168.28.126",
                      "ap_mac": "C0:8C:60:29:97:D4", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. principal: 1º Andar - Frente a SL 127", "ap_patrimony": "224010",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224016.wifi.ufsm.br", "ap_sysname": "ap-224016", "ap_ip": "192.168.28.117",
                      "ap_mac": "E4:C7:22:B2:D0:6C", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. principal: 1º Andar - Frente a SL 119", "ap_patrimony": "224016",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224017.wifi.ufsm.br", "ap_sysname": "ap-224017", "ap_ip": "192.168.28.120",
                      "ap_mac": "E4:C7:22:B2:D0:79", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. principal: 1º Andar - Frente a Lancheria", "ap_patrimony": "224017",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224005.wifi.ufsm.br", "ap_sysname": "ap-224005", "ap_ip": "192.168.28.131",
                      "ap_mac": "C0:67:AF:CA:B2:ED", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. principal: 2º Andar - Frente a SL 232", "ap_patrimony": "224005",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224006.wifi.ufsm.br", "ap_sysname": "ap-224006", "ap_ip": "192.168.28.123",
                      "ap_mac": "C0:8C:60:29:98:5A", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. principal: 2º Andar - Frente a SL 222", "ap_patrimony": "224006",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224007.wifi.ufsm.br", "ap_sysname": "ap-224007", "ap_ip": "192.168.28.130",
                      "ap_mac": "C0:8C:60:29:98:3D", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. principal: 2º Andar - Frente a SL 216", "ap_patrimony": "224007",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224008.wifi.ufsm.br", "ap_sysname": "ap-224008", "ap_ip": "192.168.28.132",
                      "ap_mac": "C0:8C:60:29:98:31", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. principal: 2º Andar - Frente a SL 205", "ap_patrimony": "224008",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224001.wifi.ufsm.br", "ap_sysname": "ap-224001", "ap_ip": "192.168.28.125",
                      "ap_mac": "E4:C7:22:B2:D0:7C", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. principal: 3º Andar - Frente a SL 335", "ap_patrimony": "224001",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224002.wifi.ufsm.br", "ap_sysname": "ap-224002", "ap_ip": "192.168.28.127",
                      "ap_mac": "C0:67:AF:CA:B2:DB", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. principal: 3º Andar - Frente a SL 322", "ap_patrimony": "224002",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224003.wifi.ufsm.br", "ap_sysname": "ap-224003", "ap_ip": "192.168.28.124",
                      "ap_mac": "E4:C7:22:B2:CF:A8", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. principal: 3º Andar - Frente a SL 317", "ap_patrimony": "224003",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224004.wifi.ufsm.br", "ap_sysname": "ap-224004", "ap_ip": "192.168.28.129",
                      "ap_mac": "C0:67:AF:CA:B2:5F", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. principal: 3º Andar - Frente a SL 304", "ap_patrimony": "224004",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224018.wifi.ufsm.br", "ap_sysname": "ap-224018", "ap_ip": "192.168.28.115",
                      "ap_mac": "E4:C7:22:B2:D0:5F", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. principal: 1º andar -  Auditório Pércio Reis", "ap_patrimony": "224018",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228333.wifi.ufsm.br", "ap_sysname": "ap-228333", "ap_ip": "192.168.28.60",
                      "ap_mac": "D0:72:DC:09:04:FF", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CT - P. Anexo A 1º Andar-1", "ap_patrimony": "228333", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228353.wifi.ufsm.br", "ap_sysname": "ap-228353", "ap_ip": "192.168.28.73",
                      "ap_mac": "00:22:BD:FE:56:D5", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CT - P. Anexo A 2º Andar-1", "ap_patrimony": "228353", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228352.wifi.ufsm.br", "ap_sysname": "ap-228352", "ap_ip": "192.168.28.72",
                      "ap_mac": "00:22:BD:FE:56:D7", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CT - P. Anexo A 3º Andar-1", "ap_patrimony": "228352", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228351.wifi.ufsm.br", "ap_sysname": "ap-228351", "ap_ip": "192.168.28.74",
                      "ap_mac": "00:22:BD:FE:56:9E", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CT - P. Anexo A 3º Andar-2", "ap_patrimony": "228351", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228336.wifi.ufsm.br", "ap_sysname": "ap-228336", "ap_ip": "192.168.28.56",
                      "ap_mac": "D0:72:DC:1E:1B:80", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CT - P. Anexo A 1º Andar-2", "ap_patrimony": "228336", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228354.wifi.ufsm.br", "ap_sysname": "ap-228354", "ap_ip": "192.168.28.71",
                      "ap_mac": "00:22:BD:FE:56:9B", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CT - P. Anexo A 2º Andar-2", "ap_patrimony": "228354", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224019.wifi.ufsm.br", "ap_sysname": "ap-224019", "ap_ip": "192.168.28.119",
                      "ap_mac": "E4:C7:22:B2:D0:A5", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. Anexo A 2º andar / corredor ao lado do elevador",
                      "ap_patrimony": "224019", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228348.wifi.ufsm.br", "ap_sysname": "ap-228348", "ap_ip": "192.168.28.67",
                      "ap_mac": "3C:08:F6:47:1E:89", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CT - P. Anexo C 1º Andar-1", "ap_patrimony": "228348", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228347.wifi.ufsm.br", "ap_sysname": "ap-228347", "ap_ip": "192.168.28.68",
                      "ap_mac": "00:22:BD:FE:56:3D", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CT - P. Anexo C 2º Andar-1", "ap_patrimony": "228347", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228350.wifi.ufsm.br", "ap_sysname": "ap-228350", "ap_ip": "192.168.28.77",
                      "ap_mac": "00:22:BD:FE:56:EC", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CT - P. Anexo C 3º Andar-2", "ap_patrimony": "228350", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228349.wifi.ufsm.br", "ap_sysname": "ap-228349", "ap_ip": "192.168.28.66",
                      "ap_mac": "D0:72:DC:09:04:B5", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CT - P. Anexo C 2º Andar-2", "ap_patrimony": "228349", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228341.wifi.ufsm.br", "ap_sysname": "ap-228341", "ap_ip": "192.168.28.75",
                      "ap_mac": "00:22:BD:FE:56:E7", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CT - P. Anexo C 3º Andar-1", "ap_patrimony": "228341", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228340.wifi.ufsm.br", "ap_sysname": "ap-228340", "ap_ip": "192.168.28.76",
                      "ap_mac": "00:22:BD:FE:56:FB", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CT - P. Anexo C 1º Andar-2", "ap_patrimony": "228340", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228334.wifi.ufsm.br", "ap_sysname": "ap-228334", "ap_ip": "192.168.28.58",
                      "ap_mac": "3C:08:F6:47:1E:C0", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CT - P. Anexo C 2º andar / Auditório palco", "ap_patrimony": "228334",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224020.wifi.ufsm.br", "ap_sysname": "ap-224020", "ap_ip": "192.168.28.113",
                      "ap_mac": "E4:C7:22:B2:D0:76", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. Anexo A 1º Andar PRO+E", "ap_patrimony": "224020", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224041.wifi.ufsm.br", "ap_sysname": "ap-224041", "ap_ip": "192.168.28.118",
                      "ap_mac": "C0:67:AF:E4:00:37", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CTLAB / NUPEDEE", "ap_patrimony": "224041", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224042.wifi.ufsm.br", "ap_sysname": "ap-224042", "ap_ip": "192.168.28.116",
                      "ap_mac": "E4:C7:22:B2:D0:7F", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CT - P. Prédio 09E", "ap_patrimony": "224042", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224043.wifi.ufsm.br", "ap_sysname": "ap-224043", "ap_ip": "192.168.28.122",
                      "ap_mac": "C0:67:AF:CA:B2:2B", "ap_model": "AIR-CAP1602I-T-K9", "ap_location": "Prédio 09E",
                      "ap_patrimony": "224043", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224044.wifi.ufsm.br", "ap_sysname": "ap-224044", "ap_ip": "192.168.28.121",
                      "ap_mac": "C0:67:AF:CA:B1:FD", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "Prédio Principal / 3º Andar - NCC Frente a SL 339", "ap_patrimony": "224044",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224045.wifi.ufsm.br", "ap_sysname": "ap-224045", "ap_ip": "192.168.28.114",
                      "ap_mac": "C0:67:AF:E4:04:45", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "Prédio Principal / 3 Andar - NIC SL 301", "ap_patrimony": "224045",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224051.wifi.ufsm.br", "ap_sysname": "ap-224051", "ap_ip": "192.168.28.192",
                      "ap_mac": "C0:67:AF:E4:04:8E", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "CTLAB / DESA - 2º Andar", "ap_patrimony": "224051", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224052.wifi.ufsm.br", "ap_sysname": "ap-224052", "ap_ip": "192.168.28.193",
                      "ap_mac": "E4:C7:22:B2:D0:72", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "Anexo A 3º Andar - Auditório SL 355", "ap_patrimony": "224052", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224053.wifi.ufsm.br", "ap_sysname": "ap-224053", "ap_ip": "192.168.28.194",
                      "ap_mac": "E4:C7:22:B2:D0:45", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "Anexo C - Biblioteca", "ap_patrimony": "224053", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224037.wifi.ufsm.br", "ap_sysname": "ap-224037", "ap_ip": "192.168.28.237",
                      "ap_mac": "E4:C7:22:B2:D0:85", "ap_model": "AIR-CAP1602I-T-K9", "ap_location": "NaN",
                      "ap_patrimony": "224037", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237419.wifi.ufsm.br", "ap_sysname": "ap-237419", "ap_ip": "192.168.28.253",
                      "ap_mac": "F8:C2:88:C0:46:71", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "NaN",
                      "ap_patrimony": "237419", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237407.wifi.ufsm.br", "ap_sysname": "ap-237407", "ap_ip": "192.168.28.168",
                      "ap_mac": "F4:CF:E2:AC:29:A2", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "NÃO INSTALADO",
                      "ap_patrimony": "237407", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237408.wifi.ufsm.br", "ap_sysname": "ap-237408", "ap_ip": "192.168.28.169",
                      "ap_mac": "F4:CF:E2:B9:18:FF", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "NÃO INSTALADO",
                      "ap_patrimony": "237408", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237432.wifi.ufsm.br", "ap_sysname": "ap-237432", "ap_ip": "192.168.28.202",
                      "ap_mac": "74:A0:2F:7D:98:B3", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CRECHE - Rack corredor / fibra", "ap_patrimony": "237432", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237433.wifi.ufsm.br", "ap_sysname": "ap-237433", "ap_ip": "192.168.28.203",
                      "ap_mac": "F4:CF:E2:1C:63:A8", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CRECHE - Rack corredor / fibra", "ap_patrimony": "237433", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224046.wifi.ufsm.br", "ap_sysname": "ap-224046", "ap_ip": "192.168.28.52",
                      "ap_mac": "E4:C7:22:B2:D0:C8", "ap_model": "AIR-CAP1602I-T-K9", "ap_location": "NaN",
                      "ap_patrimony": "224046", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224048.wifi.ufsm.br", "ap_sysname": "ap-224048", "ap_ip": "192.168.28.54",
                      "ap_mac": "E4:C7:22:B2:D0:AD", "ap_model": "AIR-CAP1602I-T-K9", "ap_location": "NaN",
                      "ap_patrimony": "224048", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224049.wifi.ufsm.br", "ap_sysname": "ap-224049", "ap_ip": "192.168.28.53",
                      "ap_mac": "E4:C7:22:B2:D0:1B", "ap_model": "AIR-CAP1602I-T-K9", "ap_location": "NaN",
                      "ap_patrimony": "224049", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224050.wifi.ufsm.br", "ap_sysname": "ap-224050", "ap_ip": "192.168.28.51",
                      "ap_mac": "C0:67:AF:CA:B2:59", "ap_model": "AIR-CAP1602I-T-K9", "ap_location": "NaN",
                      "ap_patrimony": "224050", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext-226779.wifi.ufsm.br", "ap_sysname": "ap-ext-226779", "ap_ip": "192.168.28.172",
         "ap_mac": "18:9C:5D:8E:A8:00", "ap_model": "AIR-CAP-1552E-N-K9", "ap_location": "NaN",
         "ap_patrimony": "226779", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext-237446.wifi.ufsm.br", "ap_sysname": "ap-ext-237446", "ap_ip": "192.168.28.137",
         "ap_mac": "0C:F5:A4:96:C2:1C", "ap_model": "AIR-CAP1552E-N-K9", "ap_location": "Planetário",
         "ap_patrimony": "237446", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext-237450.wifi.ufsm.br", "ap_sysname": "ap-ext-237450", "ap_ip": "192.168.28.139",
         "ap_mac": "0C:F5:A4:96:D4:BC", "ap_model": "AIR-CAP1552E-N-K9", "ap_location": "Multiuso",
         "ap_patrimony": "237450", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext05-237452.wifi.ufsm.br", "ap_sysname": "ap-ext05-237452", "ap_ip": "192.168.28.136",
         "ap_mac": "0C:F5:A4:96:98:1C", "ap_model": "AIR-CAP1552E-N-K9", "ap_location": "RU I",
         "ap_patrimony": "237452", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext-237445.wifi.ufsm.br", "ap_sysname": "ap-ext-237445", "ap_ip": "192.168.28.138",
         "ap_mac": "0C:F5:A4:96:BE:FC", "ap_model": "AIR-CAP1552E-N-K9", "ap_location": "RU II",
         "ap_patrimony": "237445", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext-237448.wifi.ufsm.br", "ap_sysname": "ap-ext-237448", "ap_ip": "192.168.28.140",
         "ap_mac": "BC:16:F5:1A:15:1C", "ap_model": "AIR-CAP2602E-T-K9", "ap_location": "Frederico Westphalen",
         "ap_patrimony": "237448", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext-226777.wifi.ufsm.br", "ap_sysname": "ap-ext-226777", "ap_ip": "192.168.28.173",
         "ap_mac": "18:9C:5D:8E:C7:DC", "ap_model": "AIR-CAP1552E-N-K9",
         "ap_location": "WIFI ABERTA / FIESTA MULTIWEB", "ap_patrimony": "226777", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext-237443.wifi.ufsm.br", "ap_sysname": "ap-ext-237443", "ap_ip": "192.168.28.187",
         "ap_mac": "BC:16:F5:1A:2D:C0", "ap_model": "0", "ap_location": "União - parede lateral esquerda",
         "ap_patrimony": "237443", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext-226780.ctism.ufsm.br", "ap_sysname": "ap-ext-226780", "ap_ip": "200.132.24.3",
         "ap_mac": "18:9C:5D:8E:D0:BC", "ap_model": "AIR-CAP1552E-N-K9",
         "ap_location": "Prédio de redes frente para o INPE", "ap_patrimony": "226780", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext-226776.wifi.ufsm.br", "ap_sysname": "ap-ext-226776", "ap_ip": "192.168.28.189",
         "ap_mac": "18:9C:5D:8E:AC:5C", "ap_model": "AIR-CAP1552E-N-K9", "ap_location": "Parede CTLAB entre o INPE",
         "ap_patrimony": "226776", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext-226778.wifi.ufsm.br", "ap_sysname": "ap-ext-226778", "ap_ip": "192.168.28.188",
         "ap_mac": "18:9C:5D:8E:D1:BC", "ap_model": "AIR-CAP1552E-N-K9", "ap_location": "Frente ao CCNE",
         "ap_patrimony": "226778", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext-228301.wifi.ufsm.br", "ap_sysname": "ap-ext-228301", "ap_ip": "192.168.28.229",
         "ap_mac": "1C:1D:86:34:1A:A0", "ap_model": "AIR-CAP1552E-N-K9", "ap_location": "FRENTE A BC",
         "ap_patrimony": "228301", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231041.wifi.ufsm.br", "ap_sysname": "ap-231041", "ap_ip": "192.168.28.196",
                      "ap_mac": "88:F0:31:8C:0A:DB", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "HALL 18-BASE",
                      "ap_patrimony": "231041", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231042.wifi.ufsm.br", "ap_sysname": "ap-231042", "ap_ip": "192.168.28.197",
                      "ap_mac": "88:F0:31:8C:0A:DE", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "Subsolo 18-BASE", "ap_patrimony": "231042", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231048.wifi.ufsm.br", "ap_sysname": "ap-231048", "ap_ip": "192.168.28.152",
                      "ap_mac": "88:F0:31:68:F0:F5", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "NaN",
                      "ap_patrimony": "231048", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231049.wifi.ufsm.br", "ap_sysname": "ap-231049", "ap_ip": "192.168.28.153",
                      "ap_mac": "88:F0:31:80:D9:D9", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "NaN",
                      "ap_patrimony": "231049", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231038.wifi.ufsm.br", "ap_sysname": "ap-231038", "ap_ip": "192.168.28.155",
                      "ap_mac": "88:F0:31:8C:0A:DA", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "HALL DO PRÉDIO BASE17", "ap_patrimony": "231038", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231039.wifi.ufsm.br", "ap_sysname": "ap-231039", "ap_ip": "192.168.28.156",
                      "ap_mac": "88:F0:31:68:F0:DC", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "Auditório A BASE17", "ap_patrimony": "231039", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-231040.wifi.ufsm.br", "ap_sysname": "ap-231040", "ap_ip": "192.168.28.157",
                      "ap_mac": "88:F0:31:8C:0A:05", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "Auditório B BASE17", "ap_patrimony": "231040", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228363.wifi.ufsm.br", "ap_sysname": "ap-228363", "ap_ip": "192.168.28.226",
                      "ap_mac": "D0:72:DC:09:04:B3", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "62A - Centro de Convenções - Setor ADM - 4º andar", "ap_patrimony": "228363",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-235903.wifi.ufsm.br", "ap_sysname": "ap-235903", "ap_ip": "192.168.28.248",
                      "ap_mac": "F8:C2:88:B4:F0:8E", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "62A - Centro de Convenções - Orquestra", "ap_patrimony": "235903",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228315.wifi.ufsm.br", "ap_sysname": "ap-228315", "ap_ip": "192.168.28.213",
                      "ap_mac": "00:22:BD:FE:56:BB", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "BC - Sala de estudos lado direito", "ap_patrimony": "228315", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228319.wifi.ufsm.br", "ap_sysname": "ap-228319", "ap_ip": "192.168.28.64",
                      "ap_mac": "3C:08:F6:47:1E:88", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "BC - Sala de estudos lado esquerdo", "ap_patrimony": "228319", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228314.wifi.ufsm.br", "ap_sysname": "ap-228314", "ap_ip": "192.168.28.212",
                      "ap_mac": "00:22:BD:FE:57:D7", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "BC - Corredor em frente à Direção", "ap_patrimony": "228314", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228316.wifi.ufsm.br", "ap_sysname": "ap-228316", "ap_ip": "192.168.28.214",
                      "ap_mac": "3C:08:F6:47:1E:BA", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "BC - Sub-solo",
                      "ap_patrimony": "228316", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237430.wifi.ufsm.br", "ap_sysname": "ap-237430", "ap_ip": "192.168.28.198",
                      "ap_mac": "F4:CF:E2:2E:6C:2F", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "26D - CCS (TO) - Hall", "ap_patrimony": "237430", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237431.wifi.ufsm.br", "ap_sysname": "ap-237431", "ap_ip": "192.168.28.199",
                      "ap_mac": "F4:CF:E2:1C:63:E1", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "26D - CCS (TO) - 2º andar", "ap_patrimony": "237431", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237427.wifi.ufsm.br", "ap_sysname": "ap-237427", "ap_ip": "192.168.28.200",
                      "ap_mac": "F4:CF:E2:D1:3A:0C", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "26 - CCS  - Hall 2º andar", "ap_patrimony": "237427", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237428.wifi.ufsm.br", "ap_sysname": "ap-237428", "ap_ip": "192.168.28.201",
                      "ap_mac": "F4:CF:E2:1C:63:FA", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "26 - CCS - Hall 4º andar", "ap_patrimony": "237428", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228307.wifi.ufsm.br", "ap_sysname": "ap-228307", "ap_ip": "192.168.28.9",
                      "ap_mac": "D0:72:DC:31:C0:BB", "ap_model": "AIR-CAP2602E-T-K9",
                      "ap_location": "26E - CCS - hall fono", "ap_patrimony": "228307", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228337.wifi.ufsm.br", "ap_sysname": "ap-228337", "ap_ip": "192.168.28.57",
                      "ap_mac": "D0:72:DC:09:04:C8", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CEFD - Rack térreo - corredor à esquerda", "ap_patrimony": "228337",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228328.wifi.ufsm.br", "ap_sysname": "ap-228328", "ap_ip": "192.168.28.174",
                      "ap_mac": "D0:72:DC:1E:1B:41", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CEFD -  Rack térreo - corredor à esquerda", "ap_patrimony": "228328",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228329.wifi.ufsm.br", "ap_sysname": "ap-228329", "ap_ip": "192.168.28.175",
                      "ap_mac": "00:22:BD:FE:57:B5", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CEFD -  Rack térreo - corredor à esquerda", "ap_patrimony": "228329",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228330.wifi.ufsm.br", "ap_sysname": "ap-228330", "ap_ip": "192.168.28.176",
                      "ap_mac": "D0:72:DC:1E:1B:5E", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CEFD -  Rack térreo - corredor à esquerda", "ap_patrimony": "228330",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228331.wifi.ufsm.br", "ap_sysname": "ap-228331", "ap_ip": "192.168.28.177",
                      "ap_mac": "D0:72:DC:09:04:E0", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CEFD -  Rack térreo - corredor à esquerda", "ap_patrimony": "228331",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228332.wifi.ufsm.br", "ap_sysname": "ap-228332", "ap_ip": "192.168.28.178",
                      "ap_mac": "D0:72:DC:1E:1B:6A", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CEFD - Rack térreo - corredor à esquerda", "ap_patrimony": "228332",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237417.wifi.ufsm.br", "ap_sysname": "ap-237417", "ap_ip": "192.168.28.165",
                      "ap_mac": "F8:C2:88:C0:46:9D", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "74B-CCSH - HALL", "ap_patrimony": "237417", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237411.wifi.ufsm.br", "ap_sysname": "ap-237411", "ap_ip": "192.168.28.159",
                      "ap_mac": "F4:CF:E2:BE:C9:06", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "74A-CCSH - Hall (Próximo lancheria", "ap_patrimony": "237411", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237413.wifi.ufsm.br", "ap_sysname": "ap-237413", "ap_ip": "192.168.28.161",
                      "ap_mac": "F4:CF:E2:1C:63:4B", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "74C-CCSH -  1º andar", "ap_patrimony": "237413", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237414.wifi.ufsm.br", "ap_sysname": "ap-237414", "ap_ip": "192.168.28.162",
                      "ap_mac": "F4:CF:E2:2E:6C:88", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "74C-CCSH -  2º andar SL 4224/4222", "ap_patrimony": "237414", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237415.wifi.ufsm.br", "ap_sysname": "ap-237415", "ap_ip": "192.168.28.163",
                      "ap_mac": "F4:CF:E2:B9:18:02", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "74D-CCSH - Térreo", "ap_patrimony": "237415", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237412.wifi.ufsm.br", "ap_sysname": "ap-237412", "ap_ip": "192.168.28.160",
                      "ap_mac": "F4:CF:E2:BE:C9:1E", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "74D-CCSH - 1º andar", "ap_patrimony": "237412", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228318.wifi.ufsm.br", "ap_sysname": "ap-228318", "ap_ip": "192.168.28.63",
                      "ap_mac": "D0:72:DC:1E:1B:85", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. principal: frente sl3179 corredor C 1º Andar Final",
                      "ap_patrimony": "228318", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228319.wifi.ufsm.br", "ap_sysname": "ap-228319", "ap_ip": "192.168.28.64",
                      "ap_mac": "3C:08:F6:47:1E:88", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. principal: frente sl3170 corredor C 1º andar entrada",
                      "ap_patrimony": "228319", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228321.wifi.ufsm.br", "ap_sysname": "ap-228321", "ap_ip": "192.168.28.62",
                      "ap_mac": "D0:72:DC:09:04:8F", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. principal: frente sl3236 corredor B 2º andar inicial",
                      "ap_patrimony": "228321", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228322.wifi.ufsm.br", "ap_sysname": "ap-228322", "ap_ip": "192.168.28.61",
                      "ap_mac": "D0:72:DC:1E:1B:7A", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. principal: frente sl3240 corredor B 2º andar final",
                      "ap_patrimony": "228322", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228338.wifi.ufsm.br", "ap_sysname": "ap-228338", "ap_ip": "192.168.28.78",
                      "ap_mac": "3C:08:F6:47:1E:A9", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. principal: frente sl3151 corredor B 1º andar final",
                      "ap_patrimony": "228338", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-228339.wifi.ufsm.br", "ap_sysname": "ap-228339", "ap_ip": "192.168.28.79",
                      "ap_mac": "3C:08:F6:47:1E:F1", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. principal: frente sl3148 (direção) corredor B 1º andar inicial",
                      "ap_patrimony": "228339", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245004.wifi.ufsm.br", "ap_sysname": "ap-245004", "ap_ip": "192.168.28.84",
                      "ap_mac": "F8:C2:88:C0:46:63", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. principal: frente sl3334A corredor B 3º andar inicial",
                      "ap_patrimony": "245004", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245005.wifi.ufsm.br", "ap_sysname": "ap-245005", "ap_ip": "192.168.28.85",
                      "ap_mac": "F8:C2:88:C0:46:30", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. principal: frente sl3339 corredor B 3º andar final",
                      "ap_patrimony": "245005", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245006.wifi.ufsm.br", "ap_sysname": "ap-245006", "ap_ip": "192.168.28.86",
                      "ap_mac": "F8:C2:88:C0:46:5E", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. principal: frente sl3195 corredor C 1º andar continuação",
                      "ap_patrimony": "245006", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245008.wifi.ufsm.br", "ap_sysname": "ap-245008", "ap_ip": "192.168.28.88",
                      "ap_mac": "F8:C2:88:C0:46:5F", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. Audiomax", "ap_patrimony": "245008", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245009.wifi.ufsm.br", "ap_sysname": "ap-245009", "ap_ip": "192.168.28.99",
                      "ap_mac": "F8:C2:88:B7:55:B1", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. Anexo Novo (Anexo B) Terreo começo corredor", "ap_patrimony": "245009",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245010.wifi.ufsm.br", "ap_sysname": "ap-245010", "ap_ip": "192.168.28.100",
                      "ap_mac": "F8:C2:88:B4:F0:78", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. Anexo Novo (Anexo B) Terreo meio do corredor", "ap_patrimony": "245010",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245011.wifi.ufsm.br", "ap_sysname": "ap-245011", "ap_ip": "192.168.28.101",
                      "ap_mac": "F8:C2:88:B7:55:98", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. Anexo Novo (Anexo B) Terreo Final do corredor", "ap_patrimony": "245011",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245012.wifi.ufsm.br", "ap_sysname": "ap-245012", "ap_ip": "192.168.28.102",
                      "ap_mac": "F8:C2:88:B7:55:99", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. Anexo Novo (Anexo B) 2º andar começo corredor", "ap_patrimony": "245012",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245013.wifi.ufsm.br", "ap_sysname": "ap-245013", "ap_ip": "192.168.28.103",
                      "ap_mac": "F8:C2:88:B7:55:9C", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. Anexo Novo (Anexo B) 2º andar meio corredor", "ap_patrimony": "245013",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245014.wifi.ufsm.br", "ap_sysname": "ap-245014", "ap_ip": "192.168.28.94",
                      "ap_mac": "F8:C2:88:B7:55:A7", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. Anexo Novo (Anexo B) 2º andar final corredor", "ap_patrimony": "245014",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245015.wifi.ufsm.br", "ap_sysname": "ap-245015", "ap_ip": "192.168.28.95",
                      "ap_mac": "F8:C2:88:B7:55:E3", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. Anexo Novo (Anexo B) 3º andar começo corredor", "ap_patrimony": "245015",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245016.wifi.ufsm.br", "ap_sysname": "ap-245016", "ap_ip": "192.168.28.96",
                      "ap_mac": "F8:C2:88:B7:55:D0", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. Anexo Novo (Anexo B) 3º andar meio corredor", "ap_patrimony": "245016",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245017.wifi.ufsm.br", "ap_sysname": "ap-245017", "ap_ip": "192.168.28.97",
                      "ap_mac": "F8:C2:88:AF:B1:2D", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. Anexo Novo (Anexo B) 3º andar final corredor", "ap_patrimony": "245017",
                      "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245018.wifi.ufsm.br", "ap_sysname": "ap-245018", "ap_ip": "192.168.28.98",
                      "ap_mac": "F8:C2:88:B7:55:DB", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. principal: frente sl3264 corredor C 2º andar começo",
                      "ap_patrimony": "245018", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245019.wifi.ufsm.br", "ap_sysname": "ap-245019", "ap_ip": "192.168.28.93",
                      "ap_mac": "F8:C2:88:B7:55:D1", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. principal: frente sl3270 corredor C 2º andar final",
                      "ap_patrimony": "245019", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245021.wifi.ufsm.br", "ap_sysname": "ap-245021", "ap_ip": "192.168.28.91",
                      "ap_mac": "F8:C2:88:B4:F0:80", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. principal: frente sl3360 corredor C 3º andar começo",
                      "ap_patrimony": "245021", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-245022.wifi.ufsm.br", "ap_sysname": "ap-245022", "ap_ip": "192.168.28.90",
                      "ap_mac": "F8:C2:88:B7:55:95", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "CE - P. principal: frente sl3366 Corredor C 3º andar final",
                      "ap_patrimony": "245022", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237401.wifi.ufsm.br", "ap_sysname": "ap-237401", "ap_ip": "192.168.28.206",
                      "ap_mac": "F4:CF:E2:9B:60:31", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "Palmeira das Missões", "ap_patrimony": "237401", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237402.wifi.ufsm.br", "ap_sysname": "ap-237402", "ap_ip": "192.168.28.207",
                      "ap_mac": "F4:CF:E2:AC:29:BE", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "Palmeira das Missões", "ap_patrimony": "237402", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237403.wifi.ufsm.br", "ap_sysname": "ap-237403", "ap_ip": "192.168.28.208",
                      "ap_mac": "F4:CF:E2:9B:60:1A", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "Palmeira das Missões", "ap_patrimony": "237403", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237404.wifi.ufsm.br", "ap_sysname": "ap-237404", "ap_ip": "192.168.28.209",
                      "ap_mac": "F4:CF:E2:B9:18:EE", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "Palmeira das Missões", "ap_patrimony": "237404", "ap_online": "1"})

    db.insert_device(
        {"ap_hostname": "ap-ext-237451.wifi.ufsm.br", "ap_sysname": "ap-ext-237451", "ap_ip": "192.168.28.210",
         "ap_mac": "0C:F5:A4:96:C0:5C", "ap_model": "AIR-CAP1552E-N-K9", "ap_location": "Palmeira das Missões",
         "ap_patrimony": "237451", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237434.wifi.ufsm.br", "ap_sysname": "ap-237434", "ap_ip": "192.168.28.204",
                      "ap_mac": "F4:CF:E2:1C:63:E8", "ap_model": "AIR-CAP2602I-T-K9",
                      "ap_location": "40A - CAL (LETRAS) - HALL", "ap_patrimony": "237434", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224040.wifi.ufsm.br", "ap_sysname": "ap-224040", "ap_ip": "192.168.28.234",
                      "ap_mac": "C0:67:AF:CA:B2:66", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "40 - CAL - P40 - Hall", "ap_patrimony": "224040", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224054.wifi.ufsm.br", "ap_sysname": "ap-224054", "ap_ip": "192.168.28.231",
                      "ap_mac": "E4:C7:22:B2:D0:84", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "40 - CAL - P40 - 3º andar (Central)", "ap_patrimony": "224054", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224039.wifi.ufsm.br", "ap_sysname": "ap-224039", "ap_ip": "192.168.28.233",
                      "ap_mac": "E4:C7:22:B2:D0:B8", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "40 - CAL - P40 - 2º andar (LD)", "ap_patrimony": "224039", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224055.wifi.ufsm.br", "ap_sysname": "ap-224055", "ap_ip": "192.168.28.232",
                      "ap_mac": "C0:67:AF:CA:B2:8F", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "40 - CAL - P40 - 2º andar (LE)", "ap_patrimony": "224055", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-224038.wifi.ufsm.br", "ap_sysname": "ap-224038", "ap_ip": "192.168.28.235",
                      "ap_mac": "E4:C7:22:B2:D0:98", "ap_model": "AIR-CAP1602I-T-K9",
                      "ap_location": "40B - CAL (MUSICA) - HALL 2º ANDAR", "ap_patrimony": "224038", "ap_online": "1"})

    db.insert_device({"ap_hostname": "ap-237418.wifi.ufsm.br", "ap_sysname": "ap-237418", "ap_ip": "192.168.28.166",
                      "ap_mac": "F8:C2:88:C0:46:97", "ap_model": "AIR-CAP2602I-T-K9", "ap_location": "PRÉDIO 67",
                      "ap_patrimony": "237418", "ap_online": "1"})
