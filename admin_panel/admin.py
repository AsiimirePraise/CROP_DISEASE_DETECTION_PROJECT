
from django.contrib import admin
from .models import SystemConfiguration, SystemLog, MaintenanceWindow, BackupRecord


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['key', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['level', 'message', 'module', 'user', 'timestamp']
    list_filter = ['level', 'module', 'timestamp']
    search_fields = ['message', 'module', 'user__email']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'


@admin.register(MaintenanceWindow)
class MaintenanceWindowAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_time', 'end_time', 'is_active', 'created_by']
    list_filter = ['is_active', 'start_time']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']


@admin.register(BackupRecord)
class BackupRecordAdmin(admin.ModelAdmin):
    list_display = ['backup_type', 'status', 'file_size', 'started_at', 'completed_at']
    list_filter = ['backup_type', 'status', 'created_at']
    search_fields = ['file_path', 'created_by__email']
    readonly_fields = ['created_at']
