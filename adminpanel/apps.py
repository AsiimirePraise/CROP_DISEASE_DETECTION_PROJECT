from django.apps import AppConfig


class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin'


class AdminpanelConfig(AppConfig):  # Changed from AdminConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adminpanel'  # Must match your app directory name