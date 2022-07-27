from django.contrib import admin
from .models import Switch, Reports, Ap, SwitchPicture


class SwitchAdmin(admin.ModelAdmin):
    # serve para mostrar as colunas desejadas na interface do django admin
    list_display = ('ip', 'name', 'mac')


class DhcpAdmin(admin.ModelAdmin):
    list_display = ('dhcp_mac', 'dhcp_name')


class VlanAdmin(admin.ModelAdmin):
    list_display = ('vlan_id', 'vlan_name')


class NetworkAddressAdmin(admin.ModelAdmin):
    list_display = ('network_address', 'network_mask', 'network_gateway')


class NetMapAdmin(admin.ModelAdmin):
    list_display = ('sysname', 'hostname', 'port', 'remote_port', 'remote_hostname')


class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'vendor', 'model')


class ReportsAdmin(admin.ModelAdmin):
    list_display = ('order', 'date_last_backup', 'date_last_ping', 'date_last_scan')


class ApAdmin(admin.ModelAdmin):
    list_display = ('ap_sysname', 'ap_mac', 'ap_ip', 'ap_model', 'ap_location', 'ap_online', 'ap_last_modified')


class SwitchPictureAdmin(admin.ModelAdmin):
    list_display = ('name', 'st_picture')


admin.site.register(Switch, SwitchAdmin)
admin.site.register(Reports, ReportsAdmin)
admin.site.register(Ap, ApAdmin)
admin.site.register(SwitchPicture, SwitchPictureAdmin)
