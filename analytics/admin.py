
from django.contrib import admin
from .models import AnalyticsReport, DiseaseStatistics, UserActivityLog, RegionalData, TrendAnalysis


@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'generated_by', 'date_range_start', 'date_range_end', 'created_at']
    list_filter = ['report_type', 'created_at']
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'


@admin.register(DiseaseStatistics)
class DiseaseStatisticsAdmin(admin.ModelAdmin):
    list_display = ['disease', 'crop', 'region', 'month', 'year', 'occurrence_count', 'severity_average']
    list_filter = ['year', 'month', 'disease', 'crop']
    search_fields = ['disease__name', 'crop__name', 'region']


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'timestamp', 'ip_address']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['timestamp']


@admin.register(RegionalData)
class RegionalDataAdmin(admin.ModelAdmin):
    list_display = ['region_name', 'country', 'total_users', 'total_diagnoses', 'updated_at']
    list_filter = ['country', 'climate_type']
    search_fields = ['region_name', 'country', 'state_province']
    filter_horizontal = ['primary_crops']


@admin.register(TrendAnalysis)
class TrendAnalysisAdmin(admin.ModelAdmin):
    list_display = ['title', 'trend_type', 'significance_score', 'start_date', 'end_date', 'created_at']
    list_filter = ['trend_type', 'significance_score', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['regions_affected', 'crops_affected', 'diseases_involved']
