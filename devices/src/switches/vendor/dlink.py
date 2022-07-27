import time
from paramiko import ssh_exception
from devices.src.switches.switch import Switch
import re
import devices.database.path_of_files as path_pass
from colorama import Fore
import netmiko
import telnetlib


class Dlink(Switch):
    """def get_mac_switch_by_snmp(self):
        pass"""

    def get_lldp_by_snmp(self):
        neig_port = self.snmp.snmp_walk("1.0.8802.1.1.2.1.4.1.1.7")
        all_neig: list = []
        for n_p in neig_port:
            id_neigs = n_p.oid.split('iso.0.8802.1.1.2.1.4.1.1.7.')[1]
            neig_sysname = self.snmp.snmp_get("1.0.8802.1.1.2.1.4.1.1.9." + id_neigs)
            remote_port = self.snmp.snmp_get("iso.0.8802.1.1.2.1.4.1.1.7." + id_neigs)

            local_port = id_neigs.split('.')[-2]

            neighbours = {
                "local_port": local_port,
                "remote_port": remote_port,
                "neighbour_sysname": neig_sysname
            }

            all_neig.append(neighbours)
        return all_neig

    """ def get_mac_table(self):
        pass """

    def get_interfaces_by_snmp(self):
        # como tem vários modelos, é preciso testar um de cada

        try:
            walk = self.snmp.snmp_walk('ifName')
        except SystemError:
            print(f"Algo deu errado com o SNMP. Verifique a conectividade com o dispositivo que está tentando acessar")
            return None
        resp: list = []

        if self.model == 'DGS-3224TGR' or self.model == "DES-3200":
            for item in walk:
                # print(f'OID: {item.oid}  oid_index: {item.oid_index}  snmp_type: {item.snmp_type}  value: {item.value}')
                # normaliza o nome
                if re.search('Tag', item.value, re.IGNORECASE) is None:
                    if '/' in item.value:
                        linha = re.findall(
                            r'/[0-9]{1,2}', item.value, flags=re.IGNORECASE)[0].strip('/')
                        resp.append(linha)
                    else:
                        try:
                            linha = re.findall(
                                r'[0-9]{1,2}', item.value, flags=re.IGNORECASE)[0]
                            resp.append(linha)
                        except IndexError:
                            pass
            return resp
        else:
            for item in walk:
                # print(f'OID: {item.oid}  oid_index: {item.oid_index}  snmp_type: {item.snmp_type}  value: {item.value}')
                # normaliza o nome
                try:
                    linha = re.findall(
                        r'[0-9]{1,2}\/[0-9]{1,2}', item.value, flags=re.IGNORECASE)[0]
                    resp.append(linha.split('/')[1])
                except IndexError:
                    pass
            return resp

    def remote_access_telnet(self):
        host = self.ip
        username = 'admin'
        password = path_pass.ST_DEFAULT
        name = self.get_name()

        device = {
            'device_type': 'dlink_ds_telnet',
            'host': host,
            'username': username,
            'password': password,
        }

        print(f"\nConectando ao Switch {host} {name} ...")
        conn = netmiko.ConnectHandler(**device)
        return conn

    def remote_access_ssh(self):
        host = self.ip
        username = 'admin'
        password = path_pass.ST_DEFAULT
        name = self.get_name()
        model = self.get_model()
        sysname = self.get_sysname()
        model = self.get_model()
        vendor = self.get_vendor()
        name_backup = self.name_bkp(sysname, vendor, model)

        device = {
            'device_type': 'dlink_ds',
            'host': host,
            'username': username,
            'password': password,
        }

        try:
            print(f"\nConectando ao Switche {host} {name}...")
            conn = netmiko.ConnectHandler(**device)
        except KeyboardInterrupt:
            print(Fore.RED + 'Interrompido pelo Administrador' + Fore.RESET)
            return False
        except netmiko.ssh_exception.NetmikoTimeoutException:
            print(Fore.RED + f'Não foi possível conectar no switch {name} SSH Exception' + Fore.RESET)
            conn = self.remote_access_telnet()
            # return False
        except netmiko.ssh_exception.NetmikoAuthenticationException:
            print(Fore.RED + f'Senha incorreta para o switch {name} SSH Autentication Excepton!' + Fore.RESET)
            return False
        except ssh_exception.AuthenticationException:
            print(Fore.RED + f'Senha incorreta para o switch {name} SSH Autentication Excepton!' + Fore.RESET)
            return False
        except ssh_exception.SSHException:
            print(Fore.RED + f'Erro de verificação na senha SSH para o switch {name}' + Fore.RESET)
            return False

        return conn

    def backup_configuration(self):
        host = self.ip
        username = 'admin'
        password = path_pass.ST_DEFAULT
        name = self.get_name()
        sysname = self.get_sysname()
        model = self.get_model()
        vendor = self.get_vendor()
        name_backup = self.name_bkp(sysname, vendor, model)
        """
        preciso fazer esse teste, por causa de alguns firmwares desatualizados  
        """
        test = False
        hosts_bad_firmware: list = ['192.168.5.5', '192.168.5.9', '192.168.9.5', '192.168.12.31', '192.168.18.2']
        if host in hosts_bad_firmware:
            test = True

        if model == 'DES-3028' or model == 'DES-3028P':
            try:
                conn = self.remote_access_ssh()
                print(f"\nIniciando backup...")
                interface = conn.send_command('upload cfg_toTFTP ' + path_pass.telnet_server + ' ' + name_backup)
                print(interface)
                print("########################################################")
                conn.disconnect()
                return True
            except netmiko.ssh_exception.NetmikoAuthenticationException:
                print("Erro no acesso SSH")
                return False

        elif model == 'DES-3526' or model == 'DES-3550':
            try:
                print(f"\nConectando ao Switche {host} {name}...")

                t = telnetlib.Telnet(host)  # actively connects to a telnet server
                # t.set_debuglevel(1)  # uncomment to get debug messages
                time.sleep(2)
                t.read_until(b'username:', 100)  # waits until it recieves a string 'login:'
                time.sleep(2)
                t.write(username.encode('utf-8'))  # sends username to the server
                t.write(b'\r')  # sends return character to the server
                t.read_until(b'password:', 100)  # waits until it recieves a string 'Password:'
                t.write(password.encode('utf-8'))  # sends password to the server
                t.write(b'\r')  # sends return character to the server

                print(f"\nIniciando backup...")
                command = 'upload cfg_toTFTP ' + path_pass.telnet_server + ' ' + name_backup
                t.write(command.encode('utf-8') + b'\r')  # sends a command to the server
                t.write(b'\r')
                time.sleep(5)
                t.write(b'\n\r')
                t.write(b'exit\n')
                time.sleep(1)
                t.write(b'\r')  # sends a command to the server
                t.close()

                print("Backup Concluído")
                print("########################################################")
                return True
            except:
                print(Fore.RED + f'Sem conectividade com: {name} Verificar telnet' + Fore.RESET)
                return False

        elif model == 'DES-3052' or model == 'DGS-3324SRi':
            try:
                print(f"\nConectando ao Switche {host} {name}...")

                t = telnetlib.Telnet(host)  # actively connects to a telnet server
                # t.set_debuglevel(1)  # uncomment to get debug messages
                time.sleep(2)
                t.read_until(b'UserName:', 100)  # waits until it recieves a string 'login:'
                time.sleep(2)
                t.write(username.encode('utf-8'))  # sends username to the server
                t.write(b'\r')  # sends return character to the server
                t.read_until(b'PassWord:', 100)  # waits until it recieves a string 'Password:'
                t.write(password.encode('utf-8'))  # sends password to the server
                t.write(b'\r')  # sends return character to the server

                print(f"\nIniciando backup...")
                command = 'upload cfg_toTFTP ' + path_pass.telnet_server + ' ' + name_backup
                t.write(command.encode('utf-8') + b'\r')  # sends a command to the server
                t.write(b'\r')
                time.sleep(5)
                t.write(b'\n\r')
                t.write(b'exit\n')
                time.sleep(1)
                t.write(b'\r')  # sends a command to the server
                t.close()

                print("Backup Concluído")
                print("########################################################")
                return True
            except:
                print(Fore.RED + f'Sem conectividade com: {name} Verificar telnet' + Fore.RESET)
                return False


        elif model == 'DGS-3224TGR' or test:
            device = {
                'device_type': 'dlink_ds_telnet',
                'host': host,
                'username': username,
                'password': password,
            }
            try:
                print(f"\nConectando ao Switche {host} {name}...")
                conn = netmiko.ConnectHandler(**device)
                print(f"\nIniciando backup...")
                command = 'upload configuration ' + path_pass.telnet_server + ' ' + name_backup
                print(command)
                interface = conn.send_command(command)
                print(interface)
                print("########################################################")
                conn.disconnect()
                return True
            except KeyboardInterrupt:
                print(Fore.RED + 'Interrompido pelo Administrador' + Fore.RESET)
                return False
            except netmiko.ssh_exception.NetmikoTimeoutException:
                print(Fore.RED + f'Não foi possível conectar no switch {name}' + Fore.RESET)
                return False
            except netmiko.ssh_exception.NetmikoAuthenticationException:
                print(Fore.RED + f'Senha incorreta para o switch {name}' + Fore.RESET)
                return False
            except:
                print(Fore.RED + f'Sem conectividade com: {name}' + Fore.RESET)
                return False

        elif model == 'DES-1210-28':
            device = {
                'device_type': 'dlink_ds_telnet',
                'host': host,
                'username': username,
                'password': password,
            }
            try:
                print(f"\nConectando ao Switche {host} {name}...")
                conn = netmiko.ConnectHandler(**device)
                print(f"\nIniciando backup...")
                interface = conn.send_command(
                    'upload cfg_toTFTP ' + path_pass.telnet_server + ' ' + name_backup)
                print(interface)
                print("########################################################")

                conn.disconnect()
                return True
            except KeyboardInterrupt:
                print(Fore.RED + 'Interrompido pelo Administrador' + Fore.RESET)
                return False
            except netmiko.ssh_exception.NetmikoTimeoutException:
                print(Fore.RED + f'Não foi possível conectar no switch {name}' + Fore.RESET)
                return False
            except netmiko.ssh_exception.NetmikoAuthenticationException:
                print(Fore.RED + f'Senha incorreta para o switch {name}' + Fore.RESET)
                return False
            except:
                print(Fore.RED + f'Sem conectividade com: {name}' + Fore.RESET)
                return False

        elif model == 'DES-3200' or model == 'DES-3552' or model == 'DES-3250TG':
            device = {
                'device_type': 'dlink_ds_telnet',
                'host': host,
                'username': username,
                'password': password,
            }
            try:
                print(f"\nConectando ao Switche {host} {name}...")
                conn = netmiko.ConnectHandler(**device)
                print(f"\nIniciando backup...")
                interface = conn.send_command(
                    'upload cfg_toTFTP ' + path_pass.telnet_server + ' dest_file ' + name_backup)
                print(interface)
                print("########################################################")
                conn.disconnect()
                return True
            except KeyboardInterrupt:
                print(Fore.RED + 'Interrompido pelo Administrador' + Fore.RESET)
                return False
            except netmiko.ssh_exception.NetmikoTimeoutException:
                print(Fore.RED + f'Não foi possível conectar no switch {name}' + Fore.RESET)
                return False
            except netmiko.ssh_exception.NetmikoAuthenticationException:
                print(Fore.RED + f'Senha incorreta para o switch {name}' + Fore.RESET)
                return False
            except:
                print(Fore.RED + f'Sem conectividade com: {name}' + Fore.RESET)
                return False

        elif model == 'DES-3226L':

            try:
                print(f"\nConectando ao Switche {host} {name}...")

                t = telnetlib.Telnet(host)  # actively connects to a telnet server
                # t.set_debuglevel(1)  # uncomment to get debug messages
                time.sleep(2)
                t.read_until(b'UserName:', 100)  # waits until it recieves a string 'login:'
                time.sleep(2)
                t.write(username.encode('utf-8'))  # sends username to the server
                t.write(b'\r')  # sends return character to the server
                t.read_until(b'PassWord:', 100)  # waits until it recieves a string 'Password:'
                t.write(password.encode('utf-8'))  # sends password to the server
                t.write(b'\r')  # sends return character to the server

                print(f"\nIniciando backup...")

                command = 'upload configuration ' + path_pass.telnet_server + ' ' + name_backup
                t.write(command.encode('utf-8') + b'\r')  # sends a command to the server
                t.write(b'\r')
                time.sleep(5)
                t.write(b'\n\r')
                t.write(b'exit\n')
                time.sleep(1)
                t.write(b'\r')  # sends a command to the server
                t.close()

                print("Backup Concluído")
                print("########################################################")
                return True
            except:
                print(Fore.RED + f'Sem conectividade com: {name} Verificar telnet' + Fore.RESET)
                return False

        else:
            device = {
                'device_type': 'dlink_ds_telnet',
                'host': host,
                'username': 'admin',
                'password': 'public',
            }

            try:
                print(f"\nConectando ao Switche {host} {name}...")
                conn = netmiko.ConnectHandler(**device)
                print(f"\nIniciando backup...")
                interface = conn.send_command(
                    'upload cfg_toTFTP ' + path_pass.telnet_server + ' ' + name_backup)
                print(interface)
                print("########################################################")
                conn.disconnect()

                return True
            except KeyboardInterrupt:
                print(Fore.RED + 'Interrompido pelo Administrador' + Fore.RESET)
                return False
            except netmiko.ssh_exception.NetmikoTimeoutException:
                print(Fore.RED + f'Não foi possível conectar no switch {name}' + Fore.RESET)
                return False
            except netmiko.ssh_exception.NetmikoAuthenticationException:
                print(Fore.RED + f'Senha incorreta para o switch {name}' + Fore.RESET)
                return False

    def set_ntp(self):
        print("Ainda não implementado para esse modelo")


if __name__ == "__main__":
    s_dlink = Dlink('192.168.22.132')
    resp = s_dlink.get_interfaces_by_snmp()
    print(resp)
