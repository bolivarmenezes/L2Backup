import json
import os
from django.contrib import messages
from django.core import serializers
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, FormView
from .models import Switch, Reports, Ap, SwitchPicture
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from devices.src.scan_switch import Scanner
from .src.backup_st_configurations_thread import BackupSt
from .src.mapper import SwitchMapper
from devices.database import path_of_files as path_files
from datetime import datetime, timezone
from .forms import SwitchModelForm, SwitchCreateModelForm, SwitchPictureModelForm
from .src.reports.reports import ReportsController


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['switches'] = Switch.objects.filter(disable_st='0')
        context['amount_sts'] = Switch.objects.filter(disable_st='0').count()
        last_scan = Reports.objects.filter(order='1')
        last_backup = Reports.objects.filter(order='1')
        last_scan_snmp = 'NaN'
        last_scan_icmp = 'NaN'
        last_backup_full = 'NaN'
        for last in last_scan:
            last_scan_snmp = last.date_last_scan
            last_scan_icmp = last.date_last_ping
            last_backup_full = last.date_last_backup

        context['last_scan_snmp'] = last_scan_snmp
        context['last_scan_icmp'] = last_scan_icmp
        context['last_backup_full'] = last_backup_full
        context['last_backup'] = last_backup
        context['address_server'] = path_files.tftp_server
        context['dir_bkp_sts'] = path_files.dir_bkp_sts

        # dispositivo sem backup
        context['no_backup'] = Switch.objects.filter(last_backup='NaN').count()
        # backups em dia (considerando uma vez por dia)
        date = datetime.now()
        date_today = date.strftime('%d/%m/%Y')
        count = 0
        count2 = 0
        all_data = Switch.objects.order_by('name').filter(disable_st='0')

        for st in all_data:
            date_db = st.last_backup.split(' ')[0]
            if date_db == date_today:
                count += 1
            else:
                count2 += 1

        context['amount_backups_ok'] = count
        context['amount_old_backups'] = count2
        context['switches'] = all_data
        context['amount_switches_off'] = Switch.objects.filter(
            online='0').count()

        return context

    def post(self, request, *args, **kwargs):
        action = kwargs['action']
        if action == 'backup_all_st':
            # realiza backup de todos os switches
            backup = BackupSt()
            response = backup.backup_conf()
            print(response)
            response = json.dumps('backup_all_st Realizado com sucesso')
            return HttpResponse(response, content_type='application/json')
        elif action == 'scan_all_st':
            # scaneia, via SNMP, todos os switches
            scan = Scanner()
            response = scan.scan_switch()
            print(response)
            response = json.dumps('scan_all_st Realizado com sucesso')
            return HttpResponse(response, content_type='application/json')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SwitchView(TemplateView, View):
    template_name = 'switch.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SwitchView, self).get_context_data(**kwargs)
        context['switches'] = Switch.objects.filter(disable_st='0')
        context['amount_sts'] = Switch.objects.filter(disable_st='0').count()
        last_scan = Reports.objects.filter(order='1')
        for last in last_scan:
            last_scan = last.date_last_scan
        context['last_scan'] = last_scan
        return context

    def post(self, *args, **kwargs):
        ip = kwargs['ipSwitchUpdate']
        scan = Scanner(ip)
        scan.scan_switch()
        response = json.dumps('deu certo')
        return HttpResponse(response, content_type='application/json')


class SwitchesOffView(TemplateView):
    template_name = 'switches_off.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SwitchesOffView, self).get_context_data(**kwargs)
        context['switches'] = Switch.objects.all()
        last_ping = Reports.objects.filter(order='1')
        for last in last_ping:
            last_ping = last.date_last_ping
        context['last_ping'] = last_ping

        print(context['last_ping'])

        context['amount_switches_off'] = Switch.objects.filter(
            online='0').count()

        return context


class SwitchesOffViewDelete(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        ip_st = kwargs['ipSwitchDisable']
        try:
            Switch.objects.filter(ip=ip_st).update(disable_st='1')
            response = f'Switch {ip_st} desabilitado com sucesso'
        except:
            response = f'Algo errado não está certo. Verifique (nas viwes)!'

        return HttpResponse(response, content_type='application/json')


class SwitchesNewView(FormView):
    template_name = 'switches_new.html'
    model = Switch
    form_class = SwitchModelForm
    success_url = reverse_lazy('switches_new')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SwitchesNewView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form, *args, **kwargs):
        form = dict(form.data)
        data_form: list = []
        for chave, valor in form.items():
            data_form.append(valor[0])

        command = self.type_vendor(data_form)
        print(command)
        # messages.success(self.request, 'Novo Switch criado com sucesso!')
        return super(SwitchesNewView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Novo Switch criado com sucesso!')
        return super(SwitchesNewView, self).form_invalid(form, *args, **kwargs)


class SwitchesBackupView(TemplateView):
    template_name = 'switches_backup.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SwitchesBackupView, self).get_context_data(**kwargs)
        last_backup = Reports.objects.filter(order='1')
        for last in last_backup:
            last_backup = last.date_last_backup
            last_scan = last.date_last_scan
        context['last_backup'] = last_backup
        # dispositivo sem backup
        context['no_backup'] = Switch.objects.filter(last_backup='NaN').count()
        # backups em dia (considerando uma vez por dia)
        date = datetime.now()
        date_today = date.strftime('%d/%m/%Y')
        count = 0
        count2 = 0
        count3 = 0
        all_data = Switch.objects.order_by('name').filter(disable_st='0')

        for st in all_data:
            date_db = st.last_backup.split(' ')[0]
            if date_db == date_today:
                count += 1
            else:
                count2 += 1
            count3 += 1
        context['amount_backups_ok'] = count
        context['amount_old_backups'] = count2
        context['amount_of_backups'] = count3
        context['switches'] = all_data
        try:
            context['last_scan'] = last_scan
        except UnboundLocalError:
            context['last_scan'] = "NaN"

        return context

    def post(self, request, *args, **kwargs):
        ip_name = kwargs['ipSwitchBackup'].split('_')[1]
        action = kwargs['action']
        if action == 'backup_st':
            # realiza backup
            backup = BackupSt(ip_name)
            backup.backup_conf()
            response = json.dumps('deu certo')
            return HttpResponse(response, content_type='application/json')
        elif action == 'download_backup_st':
            name_file = str(ip_name).split('.')[0]

            # 3
            # gambiarra para resolver as exceções dos MGMT
            if 'st-ufsm-09a' in ip_name:
                name_file = 'st-ufsm-09a'
            if 'st-ufsm-09b' in ip_name:
                name_file = 'st-ufsm-09b'
            if 'st-cloud-00' in ip_name:
                name_file = 'st-cloud-00'
            # 3

            # restaura backup
            list_of_files = self.get_all_files_and_date(name_file)
            if list_of_files == '0':
                response = json.dumps(
                    'Nenhum backup encontrado para esse  switch!')
            else:
                lines: list = []
                for k, v in list_of_files.items():
                    date_bkp = str(v)
                    lines.append({'path': k, 'date_bkp': date_bkp})

                response = json.dumps(lines)
            return HttpResponse(response, content_type='application/json')

    def get_all_files_and_date(self, name) -> dict:
        path_dir = path_files.path_dir + name + '/'
        file_and_date: dict = {}
        # testa se existe arquivo de backup
        exist = os.path.exists(path_dir)
        if exist is False:
            return '0'
        else:
            # organize em ordem alfabética reversa (por data)
            lsfiles = sorted(os.listdir(path_dir), reverse=True)
            for file in lsfiles:
                try:
                    cfg = file.split('.')[1]
                    if cfg == 'cfg':
                        path_file = path_dir + file
                        stat_result = os.stat(path_file)
                        date = datetime.fromtimestamp(
                            stat_result.st_mtime, tz=timezone.utc).date()
                        file_and_date["backup_st/" + name + "/" + file] = date
                except IndexError:
                    pass
            if len(file_and_date.items()) > 0:
                return file_and_date
            else:
                return '0'


class SwitchPictureView(FormView):
    template_name = 'switches_pictures.html'
    form_class = SwitchPictureModelForm
    success_url = reverse_lazy('switches_pictures')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SwitchPictureView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            form.save()

            return self.form_valid(form)
        else:
            print(form)
            return self.form_invalid(form)


class SwitchGetPictureView(View):

    def get(self, request):
        param = request.GET['param']
        datas = SwitchPicture.objects.filter(name=param)
        print(datas)
        qs_json = serializers.serialize('json', datas)
        print(qs_json)
        return HttpResponse(qs_json, content_type='application/json')


class SwitchViewFilter(View):

    def get(self, request):
        param = request.GET['param']
        datas = Switch.objects.filter(name__contains=param)
        qs_json = serializers.serialize('json', datas)
        return HttpResponse(qs_json, content_type='application/json')


class ReportsView(View):
    def post(self, *args, **kwargs):
        date_last_backup = Reports.objects.get(order='1')
        print(date_last_backup)
        response = json.dumps('')
        return HttpResponse(response, content_type='application/json')


class LocationView(TemplateView):
    template_name = 'location.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LocationView, self).get_context_data(**kwargs)
        context['sts_backbone'] = Switch.objects.filter(role='0')
        context['sts_datacenter'] = Switch.objects.filter(role='-1')
        return context

    def post(self, *args, **kwargs):
        action = kwargs['action']
        if action == 'rootNode':
            root_node: str = kwargs['name']
            print(root_node + '//////////////////////////////////////////')
            # mapeia a partir do root node
            mapp = SwitchMapper(root_node=root_node)
            mapp.mapper()
            print(root_node)

        response = json.dumps('teste')
        return HttpResponse(response, content_type='application/json')


class APsView(TemplateView):
    template_name = 'access_point.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(APsView, self).get_context_data(**kwargs)
        context['aps'] = Ap.objects.all()
        return context


class ReportsControllerView(TemplateView):
    template_name = 'reports.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReportsControllerView, self).get_context_data(**kwargs)
        rpc = ReportsController()
        context['ReportsController'] = rpc.cmpQtdSwitches()
        print(f"mongo {rpc.qtdMongo()}")
        print(f"mongo {rpc.qtdMysql()}")
        context['qtdMongo'] = rpc.qtdMongo()
        context['qtdMysql'] = rpc.qtdMysql()
        return context


class SwitchCreateView(FormView):
    template_name = 'switches_create.html'
    form_class = SwitchCreateModelForm
    success_url = reverse_lazy('switches_create')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SwitchCreateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form, *args, **kwargs):
        form.save()
        response = json.dumps('Switch cadastrado com sucesso!')
        return HttpResponse(response, content_type='application/json')

    def form_invalid(self, form, *args, **kwargs):
        form = dict(form.errors)
        data_form: list = []
        for chave, valor in form.items():
            data_form.append("<b>" + chave.upper() + "</b>: " + valor[0])
            print(chave, valor)
        response = json.dumps(data_form)
        return HttpResponse(response, content_type='application/json')
