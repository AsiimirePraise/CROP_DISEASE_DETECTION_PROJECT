
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .models import AnalyticsReport, DiseaseStatistics, TrendAnalysis, RegionalData
from diagnosis.models import DiagnosisRequest, Disease


@login_required
def analytics_dashboard_view(request):
    # Get user's diagnosis statistics
    user_diagnoses = DiagnosisRequest.objects.filter(user=request.user)
    
    # Recent trends (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_diagnoses = user_diagnoses.filter(created_at__gte=thirty_days_ago)
    
    # Basic statistics
    stats = {
        'total_diagnoses': user_diagnoses.count(),
        'recent_diagnoses': recent_diagnoses.count(),
        'completed_diagnoses': user_diagnoses.filter(status='completed').count(),
        'most_common_diseases': [],
    }
    
    # Most common diseases for the user
    if user_diagnoses.exists():
        disease_counts = Disease.objects.filter(
            diseasedetection__diagnosis_result__diagnosis_request__user=request.user
        ).annotate(
            detection_count=Count('diseasedetection')
        ).order_by('-detection_count')[:5]
        
        stats['most_common_diseases'] = disease_counts
    
    context = {
        'stats': stats,
        'recent_trends': TrendAnalysis.objects.all()[:5],
    }
    
    return render(request, 'analytics/dashboard.html', context)


@login_required
def reports_list_view(request):
    reports = AnalyticsReport.objects.filter(generated_by=request.user)
    
    return render(request, 'analytics/reports_list.html', {'reports': reports})


@login_required
def generate_report_view(request):
    # Placeholder for report generation
    return render(request, 'analytics/generate_report.html')


@login_required
def report_detail_view(request, report_id):
    report = get_object_or_404(AnalyticsReport, id=report_id, generated_by=request.user)
    
    return render(request, 'analytics/report_detail.html', {'report': report})


def trends_view(request):
    trends = TrendAnalysis.objects.all()[:10]
    
    return render(request, 'analytics/trends.html', {'trends': trends})


def regional_analysis_view(request):
    regions = RegionalData.objects.all()
    
    return render(request, 'analytics/regional.html', {'regions': regions})
