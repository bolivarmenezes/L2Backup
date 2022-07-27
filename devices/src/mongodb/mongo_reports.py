"""
Gerencia o mongo db
"""
from datetime import datetime
from pymongo import MongoClient


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

    def select_last_date(self):
        last_date = self.database.devices_reports.find_one({"date_last_backup": '1'})
        return last_date

    def update_date_last_backup(self):
        filter = {'order': '1'}
        date = datetime.now()
        date_bkp = {'date_last_backup': date.strftime('%d/%m/%Y %H:%M')}
        self.database.devices_reports.update_one(filter, {'$set': date_bkp})
        return date_bkp

    def update_date_last_ping(self):
        filter = {'order': '1'}
        date = datetime.now()
        date_ping = {'date_last_ping': date.strftime('%d/%m/%Y %H:%M')}
        self.database.devices_reports.update_one(filter, {'$set': date_ping})
        return date_ping

    def update_date_last_scan(self):
        filter = {'order': '1'}
        date = datetime.now()
        date_scan = {'date_last_scan': date.strftime('%d/%m/%Y %H:%M')}
        self.database.devices_reports.update_one(filter, {'$set': date_scan})
        return date_scan

    def insert_date_one(self):
        data = {
            'order': '1',
            'date_last_backup': 'NaN',
        }
        self.database.devices_reports.insert_one(data)


if __name__ == "__main__":
    db = Mongo()
    #db.insert_date_one()
    db.update_date_last_backup()
