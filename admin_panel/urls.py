
from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard_view, name='dashboard'),
    path('users/', views.user_management_view, name='users'),
    path('system/', views.system_settings_view, name='system'),
    path('logs/', views.system_logs_view, name='logs'),
    path('maintenance/', views.maintenance_view, name='maintenance'),
    path('backups/', views.backup_view, name='backups'),
]
