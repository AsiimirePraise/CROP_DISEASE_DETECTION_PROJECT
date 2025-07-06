
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from .models import SystemLog, MaintenanceWindow, BackupRecord
from diagnosis.models import DiagnosisRequest
from accounts.models import UserProfile

User = get_user_model()


@staff_member_required
def admin_dashboard_view(request):
    # System statistics
    stats = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'total_diagnoses': DiagnosisRequest.objects.count(),
        'recent_logs': SystemLog.objects.count(),
    }
    
    # Recent activity
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_diagnoses = DiagnosisRequest.objects.order_by('-created_at')[:5]
    recent_logs = SystemLog.objects.order_by('-timestamp')[:10]
    
    context = {
        'stats': stats,
        'recent_users': recent_users,
        'recent_diagnoses': recent_diagnoses,
        'recent_logs': recent_logs,
    }
    
    return render(request, 'admin_panel/dashboard.html', context)


@staff_member_required
def user_management_view(request):
    users = User.objects.all().order_by('-date_joined')
    
    # User type distribution
    user_types = UserProfile.objects.values('user_type').annotate(
        count=Count('user_type')
    )
    
    context = {
        'users': users,
        'user_types': user_types,
    }
    
    return render(request, 'admin_panel/users.html', context)


@staff_member_required
def system_settings_view(request):
    return render(request, 'admin_panel/system.html')


@staff_member_required
def system_logs_view(request):
    logs = SystemLog.objects.all().order_by('-timestamp')
    
    return render(request, 'admin_panel/logs.html', {'logs': logs})


@staff_member_required
def maintenance_view(request):
    maintenance_windows = MaintenanceWindow.objects.all().order_by('-start_time')
    
    return render(request, 'admin_panel/maintenance.html', {'maintenance_windows': maintenance_windows})


@staff_member_required
def backup_view(request):
    backups = BackupRecord.objects.all().order_by('-created_at')
    
    return render(request, 'admin_panel/backups.html', {'backups': backups})
