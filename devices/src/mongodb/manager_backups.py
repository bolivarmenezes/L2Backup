import devices.database.path_of_files as path_pass
import os
from datetime import datetime, timezone


class ManagerBackups:

    def __get_all_files_and_date(self) -> dict:
        path_dir = path_pass.backup_dir
        file_and_date: dict = {}
        for file in os.listdir(path_dir):
            try:
                cfg = file.split('.')[1]
                if cfg == 'cfg':
                    path_file = path_pass.backup_dir + file
                    stat_result = os.stat(path_file)
                    date = datetime.fromtimestamp(stat_result.st_mtime, tz=timezone.utc).date()
                    file_and_date[path_file] = date
            except IndexError:
                pass

        return file_and_date

    def __create_dir_if_no_exist(self, date) -> bool:
        new_dir = path_pass.backup_dir + 'bkp_' + date
        exist = os.path.exists(new_dir)
        if exist is False:
            os.system('mkdir ' + new_dir)

        return True

    def manager_bkp(self):
        file_and_date = self.__get_all_files_and_date()
        path_dir = path_pass.backup_dir
        aux = 0
        for path in file_and_date.keys():
            date = file_and_date[path]
            if aux != date:
                aux = date
                # cria o diretório
                self.__create_dir_if_no_exist(str(date))
            # move o arquivo pro diretório
            command = 'mv ' + path + ' ' + path_dir + 'bkp_' + str(date)
            os.system(command)
        #print('concluído')


if __name__ == '__main__':
    mb = ManagerBackups()
    dates = mb.manager_bkp()
