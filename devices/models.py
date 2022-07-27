from statistics import mode
from djongo import models

SNMP_COMMUNITY = [
    ('public', 'public'),
    ('public2', 'public2'),
    ('publi3c', 'public3'),

]
SNMP_VERSION = [
    (1, 'SNMP v1'),
    (2, 'SNMP v2c'),
    (3, 'SNMP v3'),
]


class Switch(models.Model):
    _id = models.ObjectIdField('_id', primary_key=True)
    ip = models.CharField('ip', max_length=50)
    mac = models.CharField('mac', max_length=50, default='NaN')
    name = models.CharField('name', max_length=50, default='NaN')
    vendor = models.CharField('vendor', max_length=50, default='NaN')
    model = models.CharField('model', max_length=50, default='NaN')
    community = models.CharField(
        'community', max_length=50, default='public', choices=SNMP_COMMUNITY)
    snmp_version = models.IntegerField(
        'snmp_version', default=2, choices=SNMP_VERSION)
    patrimony = models.CharField('patrimony', max_length=50, default='NaN')
    location = models.CharField('location', max_length=100, default='NaN')
    online = models.CharField('online', max_length=2, default='1')
    role = models.CharField('role', max_length=2, default='1')
    disable_st = models.CharField('disable_st', max_length=2, default='0')
    disable_scan = models.CharField('disable_scan', max_length=2, default='0')
    last_modified = models.CharField(
        'last_modified', max_length=500, default='NaN')
    last_backup = models.CharField(
        'last_backup', max_length=500, default='NaN')
    last_backup_error = models.CharField(
        'last_backup_error', max_length=500, default='0')


class SwitchPicture(models.Model):
    _id = models.ObjectIdField('_id', primary_key=True)
    name = models.CharField('name', max_length=50, default='NaN')
    st_picture = models.ImageField(upload_to="%Y/%m", blank=True)
    metadata_pic = models.CharField(
        'metadata_pic', max_length=100000, default='0')
    observation = models.CharField(
        'observation', max_length=10000, blank=True, default='0')


class Ap(models.Model):
    _id = models.ObjectIdField('_id', primary_key=True)
    ap_hostname = models.CharField('ap_name', max_length=50, default='0')
    ap_sysname = models.CharField('ap_name', max_length=50, default='0')
    ap_mac = models.CharField('ap_mac', max_length=17,
                              unique=True, default='0')
    ap_ip = models.CharField('ap_ip', max_length=25, default='0')
    ap_model = models.CharField('ap_model', max_length=50, default='0')
    ap_location = models.CharField('ap_location', max_length=100, default='0')
    ap_online = models.CharField('ap_online', max_length=2, default='1')
    ap_patrimony = models.CharField(
        'ap_patrimony', max_length=50, default='NaN')
    ap_last_modified = models.CharField(
        'ap_last_modified', max_length=500, default='0')


class Reports(models.Model):
    _id = models.ObjectIdField('_id', primary_key=True)
    order = models.CharField('order', max_length=3, default='1')
    date_last_backup = models.CharField(
        'date_last_backup', max_length=500, default='14/04/2000 07:37')
    date_last_ping = models.CharField(
        'date_last_ping', max_length=500, default='14/04/2000 07:37')
    date_last_scan = models.CharField(
        'date_last_scan', max_length=500, default='14/04/2000 07:37')
