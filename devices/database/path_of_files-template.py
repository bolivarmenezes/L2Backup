import os

script_dir = os.path.dirname(__file__)
dhcp_old = os.path.join(script_dir, 'dhcp_files/old/')
dhcp = os.path.join(script_dir, 'dhcp_files/new/')
db_redes = os.path.join(script_dir, 'db.redes')
logs_dir = os.path.join(script_dir,'../logs/')
template_vendors = os.path.join(script_dir, 'template_vendors.conf')
dir_templates_st = os.path.join(script_dir, 'templates_switch')
dir_bkp_sts = os.path.join(script_dir, 'backup_switches/')
path_dir = '/var/local/backup_switches/'
backup_dir = os.path.join(script_dir, 'backup_configuration/')
summary_network = os.path.join(script_dir, 'summary_network.json')
telnet_server = ''
database_pass = ''
database_user = ''
database_ip = ''
database_ufsm_addr = 'net_address'
HUAWEI = ''
ST_DEFAULT = ''
DLINK = ''
EXTREME_1 = ''
EXTREME_2 = ''
EXTREME_3 = ''
DELL = ''
