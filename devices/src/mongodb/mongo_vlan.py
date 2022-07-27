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
        self.client = MongoClient("localhost", 27017)
        self.database = self.client['Devices']

    def insert_vlan(self, vlan: dict) -> None:
        """
        :param vlan: dicionário contendo os dados do vlan
        :return: retorno da operação de inserção
        """
        try:
            if vlan is not None:
                self.database.devices_vlan.insert_one(vlan)
                print("A vlan foi adicionado com sucesso")
            else:
                raise Exception(
                    "A vlan não foi adicionada, porque o parâmetro passado é None")
        except errors.DuplicateKeyError:
            print(f'A vlan já foi adicionado anteriormente')

    def insert_many_vlans(self, vlans) -> None:
        try:
            if vlans is not None:
                self.database.devices_vlan.insert_many(vlans)
                print("As vlans foram adicionados com sucesso")
            else:
                raise Exception(
                    "As vlans não foram adicionados, porque o parâmetro passado é None")
        except errors.DuplicateKeyError:
            print(f'A(s) vlans já consta(m) na base de dados')
        except errors.BulkWriteError:
            print(
                f'Erro ao inserir vlans: \nPelo menos uma das vlans presentas no JSON, já está na base de dados')

    def select_vlan(self, ip):
        """
        :param ip: ip
        :return: retorna um dicionário
        """
        return self.database.devices_vlan.find_one({"ip": ip})

    def select_vlan_field_by_ip(self, ip: str, field: str):
        return self.database.devices_vlan.find_one({"ip": ip}, {field})

    def select_all_vlans(self):
        vlans = self.database.devices_vlan.find()
        at_least_one_item = False
        list_of_vlans: list = []
        for vlan in vlans:
            at_least_one_item = True
            list_of_vlans.append(vlan)
        if not at_least_one_item:
            return "A base de dados está vazia"
        return list_of_vlans

    def update_vlans(self, filter: dict, data: dict):
        self.database.devices_vlan.update_one(filter, {'$set': data})

    def delete_vlan(self, ip) -> None:
        """
        Deleta vlan pelo IP
        :param id_ip: ip vlan a ser deletado
        """
        self.database.devices_vlan.delete_one({"ip": id})

    def delete_field(self, ip: dict, name_field: dict):
        self.database.devices_vlan.update_one(ip, {'$unset': name_field})


if __name__ == "__main__":
    db = Mongo()
    """    with open(path_file.vlans_switch, 'r') as file_json:
        dados = json.load(file_json)

    for linha in dados:
        vlan_id = linha['vlan_id']
        try:
            vlan_name = linha['vlan_name']
        except KeyError:
            linha['vlan_name'] = 'NaN'
        try:
            vlan_network = linha['vlan_network']
        except KeyError:
            linha['vlan_network'] = 'NaN'
        try:
            vlan_desc = linha['vlan_desc']
        except KeyError:
            linha['vlan_desc'] = 'NaN'

        db.insert_vlan(linha)"""
