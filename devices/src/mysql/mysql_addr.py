import json
import mysql.connector
import devices.database.path_of_files as path_pass


class MysqlUfsmAddr:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=path_pass.database_ip,
            user=path_pass.database_user,
            password=path_pass.database_pass,
            database=path_pass.database_ufsm_addr,
        )
        self.mycursor = self.mydb.cursor()

    def get_all_switches(self):
        command = "select DISTINCT(hostname), device_id from devices where hostname like 'st%'"
        self.mycursor.execute(command)
        all_devices = self.mycursor.fetchall()
        list_devices = list = []
        for device in all_devices:
            list_devices.append([device[0], device[1]])
        return list_devices

    def summary_network(self):
        command_qtd_net_all = "select count(distinct(subnet)) as qtd_network from dhcp_network;"
        command_qtd_net_dhcp = "select count(distinct(subnet)) as qtd_network from dhcp_network where dhcp=1;"
        command_all_ips = "select net.id_network, net.name, net.subnet, count(addr.ip) as all_ips from dhcp_address as addr " \
                          "inner join dhcp_network as net on addr.id_network = net.id_network " \
                          "where net.dhcp=1 group by addr.id_network;"
        self.mycursor.execute(command_qtd_net_all)
        qtd_network = self.mycursor.fetchall()[0][0]

        self.mycursor.execute(command_qtd_net_dhcp)
        qtd_network_dhcp = self.mycursor.fetchall()[0][0]

        self.mycursor.execute(command_all_ips)
        result = self.mycursor.fetchall()

        all_data: list = [{"amount_network": qtd_network, "amount_dhcp_network": qtd_network_dhcp}]
        for res in result:
            id = res[0]
            name = res[1]
            net = res[2]
            qtd_all = res[3]

            cmd = f"select id_network, count(ip) as free_ips from dhcp_address " \
                  f"where id_device=0 and id_network = {id} group by id_network;"

            self.mycursor.execute(cmd)
            qtd_free = self.mycursor.fetchall()[0][1]

            all_data.append({"id_network": id, "name_network": name, "network": net, "amount_ips": qtd_all,
                             "amount_free_ips": qtd_free})

        # Serializing json
        json_object = json.dumps(all_data, indent=4)
        print(json_object)

        with open(path.summary_network, "w") as outfile:
            json.dump(all_data, outfile)


if __name__ == "__main__":
    mydb = MysqlUfsmAddr()
    mydb.summary_network()
