from django.urls import path
from .views import IndexView, SwitchView, SwitchesOffView, SwitchesOffViewDelete, SwitchesBackupView, ReportsView, \
    APsView, SwitchesNewView, LocationView, ReportsControllerView, SwitchCreateView, SwitchPictureView, SwitchViewFilter, SwitchGetPictureView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('index/<str:action>/', IndexView.as_view(), name='index'),
    path('switch/', SwitchView.as_view(), name='switch'),
    path('update_switch/<str:ipSwitchUpdate>/',
         SwitchView.as_view(), name='switch_update'),
    path('backup_switch/<str:ipSwitchBackup>/<str:action>/',
         SwitchesBackupView.as_view(), name='switch_backup'),
    path('switches_off/', SwitchesOffView.as_view(), name='switches_off'),
    path('switches_new/', SwitchesNewView.as_view(), name='switches_new'),
    path('switches_create/', SwitchCreateView.as_view(), name='switches_create'),
    path('switches_backups/', SwitchesBackupView.as_view(), name='switches_backups'),
    path('switches_pictures/', SwitchPictureView.as_view(), name='switches_pictures'),
    path('switches_disable/<str:ipSwitchDisable>/',
         SwitchesOffViewDelete.as_view(), name='st_disable'),
    path('access_point/', APsView.as_view(), name='access_point'),
    path('reports/', ReportsView.as_view(), name='reports'),
    path('reports_controller/', ReportsControllerView.as_view(), name='reports_controller'),
    path('location/', LocationView.as_view(), name='location'),
    path('map/<str:action>/<str:name>/', LocationView.as_view(), name='map'),
    path('update/', IndexView.as_view(), name='index_button'),
    path('filter_switch/', SwitchViewFilter.as_view(), name='switch_filter'),
    path('get_picture_switch/', SwitchGetPictureView.as_view(), name='get_picture_switch'),
]