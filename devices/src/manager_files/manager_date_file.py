import os
from datetime import datetime
import glob
from devices.src.mongodb.mongo_device import Mongo
from devices.database.path_of_files import path_dir


class ManagerDateBackups:

    def __init__(self, name: str = '0') -> None:
        self.db = Mongo()
        self.many = False
        self.path_dir = path_dir
        if name != '0':
            self.name = name
        else:
            self.many = True

    def __get_last_date(self):
        name_and_date: dict = {}
        all_paths = self.__get_path_dir()
        # para cada diretório, varre os arquivos e ordena (decrescente) por data
        for path in all_paths:
            files = glob.glob(path + '/*')
            files.sort(reverse=True)
            try:
                file_path = files[0]
                stat_result = os.path.getmtime(file_path)
                aux = str(datetime.fromtimestamp(stat_result)).replace('-', '/')[:-3]
                date = aux.split(' ')[0]
                hour = aux.split(' ')[1]
                date = date.split('/')[2] + '/' + date.split('/')[1] + '/' + date.split('/')[0]
                file = files[0].split('__')[0].split('/')[-2]
                if '.' in hour:
                    hour = hour.split('.')[0][:-3]
                name_and_date[file] = date + ' ' + hour
            except IndexError:
                # se o diretório não tem arquivo nenhum
                pass
        # print(name_and_date)

        return name_and_date

    def __get_path_dir(self):
        dir = glob.glob(self.path_dir + '/*')
        path_dir = []
        for path in dir:
            # print(path)
            path_dir.append(path)
        return path_dir

    def manager_date(self):
        name_and_date = self.__get_last_date()
        if self.many:
            for name in name_and_date.keys():
                date = name_and_date[name]
                if '.net.ufsm.br' not in name:
                    name = name + '.net.ufsm.br'
                filter = {'name': name}
                last_backup = {'last_backup': date}
                self.db.update_device(filter, last_backup)
        else:
            aux = self.name
            if '.net.ufsm.br' in aux:
                aux = self.name.replace('.net.ufsm.br', '')

            for name in name_and_date.keys():
                if name == aux:
                    # só atualiza para o nome passado no parâmetro
                    date = name_and_date[name]
                    if '.net.ufsm.br' not in name:
                        name = name + '.net.ufsm.br'

                    filter = {'name': name}
                    last_backup = {'last_backup': date}
                    db = Mongo()
                    db.update_device(filter, last_backup)
                    break


if __name__ == '__main__':
    mb = ManagerDateBackups()
    dates = mb.manager_date()

    # print(dates)
