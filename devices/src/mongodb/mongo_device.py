"""
Gerencia o mongo db
"""
from datetime import datetime
from pymongo import MongoClient
from pymongo import errors
import json


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
        device['last_modified'] = datetime.utcnow().today()
        try:
            if device is not None:
                self.database.devices_switch.insert_one(device)
                print("O dispositivo foi adicionado com sucesso")
            else:
                raise Exception(
                    "O dispositivo não foi adicionado, porque o parâmetro passado é None")
        except errors.DuplicateKeyError:
            print(f'O dispositivo já foi adicionado anteriormente')

    def insert_many_devices(self, devices) -> None:
        try:
            if devices is not None:
                self.database.devices_switch.insert_many(devices)
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
        return self.database.devices_switch.find_one({"ip": ip})

    def select_device_by_name(self, name):
        return self.database.devices_switch.find_one({"name": name})

    def select_device_field_by_ip(self, ip: str, field: str):
        return self.database.devices_switch.find_one({"ip": ip}, {field})

    def select_all_devices(self):
        devices = self.database.devices_switch.find()
        at_least_one_item = False
        list_of_devices: list = []
        for device in devices:
            at_least_one_item = True
            list_of_devices.append(device)
        if not at_least_one_item:
            return "A base de dados está vazia"
        return list_of_devices

    def update_device(self, filter: dict, data: dict):
        self.database.devices_switch.update_one(filter, {'$set': data})

    def delete_device(self, ip) -> None:
        """
        Deleta dispositivo pelo IP
        :param id_ip: ip dispositivo a ser deletado
        """
        self.database.devices_switch.delete_one({"ip": id})

    def delete_field(self, ip: dict, name_field: dict):
        self.database.devices_switch.update_one(ip, {'$unset': name_field})


if __name__ == "__main__":
    db = Mongo()
    all_dev = db.select_all_devices()
    for dev in all_dev:
        print(dev)

