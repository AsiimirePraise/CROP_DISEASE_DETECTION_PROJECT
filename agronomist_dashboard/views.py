from django.shortcuts import render
from django.utils import timezone
from django.db.models import Max
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import Diagnosis, Disease, SensorReading, TreatmentRecommendation


def dashboard(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    # Today's diagnoses
    todays_diagnoses = Diagnosis.objects.filter(
        diagnosed_at__date=today
    ).select_related('field', 'disease')[:10]
    
    # Top diseases this week
    top_diseases = Disease.objects.filter(
        diagnosis__diagnosed_at__date__gte=week_ago
    ).annotate(
        occurrence_count=Count('diagnosis')
    ).order_by('-occurrence_count')[:3]

    # Latest sensor readings
    latest_timestamps = SensorReading.objects.values('field', 'sensor_type').annotate(
        latest_recorded=Max('recorded_at')
    )

    # Pending treatment recommendations
    pending_treatments = TreatmentRecommendation.objects.filter(
        status='PENDING'
    ).select_related('diagnosis__field', 'diagnosis__disease')[:5]

    context = {
        'todays_diagnoses': todays_diagnoses,
        'top_diseases': top_diseases,
        'pending_treatments': pending_treatments,
    }
    return render(request, 'dashboard/dashboard.html', context)


def disease_reports(request):
    return render(request, 'dashboard/disease_reports.html')


def analytics(request):
    return render(request, 'dashboard/analytics.html')


def advisory(request):
    return render(request, 'dashboard/advisory.html')