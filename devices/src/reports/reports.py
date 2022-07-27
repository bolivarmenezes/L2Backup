from devices.src.mongodb.mongo_device import Mongo
import mysql.connector
import devices.database.path_of_files as path_pass


class ReportsController:

    def __init__(self) -> None:
        self.db = Mongo()
        self.devices = self.db.select_all_devices()
        self.mydb = mysql.connector.connect(
            host=path_pass.database_ip,
            user=path_pass.database_user,
            password=path_pass.database_pass,
            database=path_pass.database_observium,
        )
        self.mycursor = self.mydb.cursor()

    def switchMongo(self):
        count = 0
        list_devices: list = []
        for device in self.devices:
            count += 1
            name = device['name']
            list_devices.append(name)
        return list_devices

    def switchMysql(self):
        command = "select DISTINCT(hostname), vendor, location, sysContact from devices where hostname like 'st%' order by hostname"
        self.mycursor.execute(command)
        all_devices = self.mycursor.fetchall()
        list_devices: list = []
        for device in all_devices:
            list_devices.append(device[0])
        return list_devices

    def qtdMongo(self):
        return len(self.switchMongo())

    def qtdMysql(self):
        return len(self.switchMysql())

    def cmpQtdSwitches(self):
        stmysql = self.switchMysql()
        qtd_mysql = self.qtdMysql()
        stmongo = self.switchMongo()
        qtd_mongo = self.qtdMongo()
        response: list = []
        # Testa qual tem o maior número de dispositivos
        if qtd_mongo >= qtd_mysql:
            # pega os dados do mongo como base
            for st in stmongo:
                st_mongo = st
                if st_mongo in stmysql:
                    response.append(
                        {
                            "mysql": 'OK',
                            "mongo": st_mongo
                        }
                    )
                else:
                    response.append(
                        {
                            "mysql": 'ERRO',
                            "mongo": st_mongo
                        }
                    )
        else:
            # pega os dados do mysql como base
            for st in stmysql:
                st_mysql = st
                if st_mysql in stmysql:

                    response.append([
                        {
                            "mysql": st_mysql,
                            "mongo": 'OK'
                        }
                    ])
                else:
                    response.append(
                        {
                            "mysql": st_mysql,
                            "mongo": 'ERRO'
                        }
                    )
        return response


if __name__ == "__main__":
    rp = ReportsController()
    # rp.switchMongo()
    print(rp.cmpQtdSwitches())
