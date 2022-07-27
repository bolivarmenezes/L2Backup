from django import forms
from .models import Switch, SwitchPicture

class SwitchModelForm(forms.ModelForm):
    class Meta:
        model = Switch
        fields = ['ip', 'name', 'community', 'patrimony', 'location', 'vendor']


class SwitchCreateModelForm(forms.ModelForm):
    class Meta:
        model = Switch
        fields = ['ip', 'mac', 'name', 'vendor', 'model', 'community', 'snmp_version', 'patrimony', 'location',
                  'online', 'disable_scan']

class SwitchPictureModelForm(forms.ModelForm):
    class Meta:
        model = SwitchPicture
        fields = ['name','st_picture','metadata_pic','observation']