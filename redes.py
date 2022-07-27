import argparse
import re
from devices.src.backup_st_configurations_thread import BackupSt
from devices.src.manager_files.manager_date_file import ManagerDateBackups
from devices.src.scan_switch import Scanner
from devices.src.ntp_switch import NtpSwitch
from devices.src.lldb_huawei import LldpSwitch
from devices.src.layer7.network_tools import NetworkTools


def parser_ip(ip: str) -> bool:
    # RegEx responsável por analisar o formato de um IP
    ip_re = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    try:
        if ip_re.match(ip):
            campos = ip.split('.')
            for campo in campos:
                # testa se algum dos octetos não é número
                if not campo.isdigit():
                    print('O endereço IP informado é inválido')
                    return False
                # testa se algum dos octetos está com valor maior ou menor do que deveria
                if int(campo) > 255:
                    print('O endereço IP informado é inválido')
                    return False
                if int(campo) < 0:
                    print('O endereço IP informado é inválido')
                    return False
            return True
        else:
            print('O endereço IP informado é inválido')
            return False
    except TypeError:
        pass


parser = argparse.ArgumentParser()
parser.add_argument("--scan", dest="scanst",
                    help="Scaneia via SNMP o(s) switch(es) <ip do switch> ou all")
parser.add_argument("--fdb", dest="scanfdb",
                    help="FDB via SNMP <ip do switch> ou all")
parser.add_argument("--status", dest="status",
                    help="Verifica o status do(s) switch(es) <ip do switch> ou all")
parser.add_argument("--backup", dest="backup",
                    help="Executa o backup do(s) switch(es) <ip do switch> ou all")
parser.add_argument("--mysql", dest="parsermysql",
                    help="Se não sabe o que é, não executa!")
parser.add_argument("--map", dest="makemapjson",
                    help="Gera arquivo json", action='store_true')
parser.add_argument("--template-st", dest="templatest",
                    help="Templates para gerar portas dos switches")
parser.add_argument("--update-date", dest="updatedate", help="Atualiza a data do último backup de cada diretório",
                    action='store_true')
parser.add_argument("--ntp", dest="ntpst",
                    help="Atualizar o NTP server do(s) switch(es) <ip do switch> ou all")
parser.add_argument("--lldp", dest="lldpst",
                    help="Atualizar o LLDP do(s) switch(es) <ip do switch> ou all")
args = parser.parse_args()

if (args.scanst):
    # esqueneia todos os switches
    if (args.scanst == "all"):
        print('Buscar todos os switches')
        try:
            scan = Scanner()
            scan.scan_switch()
        except KeyboardInterrupt:
            pass
    else:
        ip = args.scanst
        if parser_ip(ip):
            scan = Scanner(ip)
            scan.scan_switch()

if (args.status):
    if (args.status == 'all'):
        # esqueneia todos os switches
        print('Status de todos os switches')
        net = NetworkTools()
        net.status_all_devices()
    else:
        ip = args.status
        if parser_ip(ip):
            print(f'Status do switch: {args.status}')
            net = NetworkTools()
            net.status_device(ip)

if (args.updatedate):
    print('Data/Hora Dowloads')
    mb = ManagerDateBackups()
    dates = mb.manager_date()

if (args.backup):
    if (args.backup == 'all'):
        # esqueneia todos os switches
        print('Status de todos os switches')
        backup = BackupSt()
        backup.backup_conf()
    else:
        ip = args.backup
        if parser_ip(ip):
            backup = BackupSt(ip)
            backup.backup_conf()

if (args.scanfdb):
    if (args.scanfdb == 'all'):
        # esqueneia todos os switches
        print('FDB de todos os switches')
        scan = Scanner()
        scan.scan_fdb()

    else:
        ip = args.scanfdb
        if parser_ip(ip):
            scan = Scanner(ip)
            scan.scan_fdb()

if (args.templatest):
    scan = Scanner()
    scan.scan_ports()

# NTP server
if (args.ntpst == "all"):
    print('NTP de todos os switches')
    try:
        ntp = NtpSwitch()
        ntp.ntp_server()
    except KeyboardInterrupt:
        pass
else:
    ip = args.ntpst
    if parser_ip(ip):
        ntp = NtpSwitch(ip)
        ntp.ntp_server()

# lldpst

if (args.lldpst == "all"):
    print('LLDP de todos os switches')
    try:
        lldp = LldpSwitch()
        lldp.lldp_conf()
    except KeyboardInterrupt:
        pass
else:
    ip = args.lldpst
    if parser_ip(ip):
        lldp = LldpSwitch(ip)
        lldp.lldp_conf()
