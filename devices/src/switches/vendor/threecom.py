from devices.src.switches.switch import Switch
import re


class Threecom(Switch):
    """
    def get_mac_switch_by_snmp(self):
        pass

    def get_lldp_by_snmp(self):
        pass

    def get_mac_table(self):
        pass"""

    def get_interfaces_by_snmp(self):
        try:
            walk = self.snmp.snmp_walk('ifName')
        except SystemError:
            print(f"Algo deu errado com o SNMP. Verifique a conectividade com o dispositivo que está tentando acessar")
            return None
        resp: list = []
        linha: str = ''

        for item in walk:
            # print(f'OID: {item.oid}  oid_index: {item.oid_index}  snmp_type: {item.snmp_type}  value: {item.value}')
            # normaliza o nome
            try:
                if re.search('Ethernet', item.value, re.IGNORECASE) or re.search('Fiber', item.value, re.IGNORECASE):
                    linha = re.findall(
                        r'[0-9]{1,2}\/[0-9]{1,2}', item.value, flags=re.IGNORECASE)[0]
                    resp.append(linha.split('/')[-1])
            except IndexError:
                pass

        return resp

    def get_vlan_by_snmp(self):
        pass

        """def backup_configuration(self):
        host = self.ip
        username = 'admin'
        password = path_pass.ST_DEFAULT
        name = self.get_name()
        sysname = self.get_sysname()

        browser = Firefox()
        browser.get('http://' + host + '/')
        user = browser.find_element_by_id('userName')
        user.send_keys('admin')
        password = browser.find_element_by_id('password')
        password.send_keys(path_pass.ST_DEFAULT)
        browser.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/input').click()

        # time.sleep(10)

        element_to_hover_over = browser.find_element_by_xpath("/html/body/form/div[1]/table/tbody/tr[5]/td/nobr")

        hover = ActionChains(browser).move_to_element(element_to_hover_over)
        hover.perform()

        browser.find_element_by_id("menuItem1_3_2").click()

        # time.sleep(5)
        # browser.find_element_by_xpath(
        #    '/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table[1]/tbody/tr/td//*[@id="rb"]').click()

        browser.get('http://' + host + '/htm/backup_d.htm')

        teste = browser.find_element_by_id('rb').click()

        server_ip = browser.find_element_by_id('serverip')
        server_ip.send_keys(path_pass.telnet_server)
        name_bkp = browser.find_element_by_id('filename')
        name_bkp.send_keys(' bkp_' + sysname + '.cfg')

        time.sleep(1)
        browser.find_element_by_id('btOK').click()"""
    def set_ntp(self):
        print("Ainda não implementado para esse modelo")

if __name__ == "__main__":
    s_hp = Threecom('192.168.22.12')
    resp = s_hp.get_interfaces_by_snmp()
    print(resp)
