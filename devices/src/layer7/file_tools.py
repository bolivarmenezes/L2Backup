import os


class FileTools:

    @staticmethod
    def create_file_if_no_exist(path_file) -> bool:
        exist = os.path.exists(path_file)
        if exist is False:
            command = 'touch ' + path_file
            print(f"Criando o seguinte arquivo: {command}")
            os.system(command)
        return True