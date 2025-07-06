
from django.db import models
from django.contrib.auth import get_user_model
from diagnosis.models import Crop, Disease

User = get_user_model()


class AnalyticsReport(models.Model):
    REPORT_TYPES = [
        ('disease_trends', 'Disease Trends'),
        ('crop_health', 'Crop Health'),
        ('treatment_effectiveness', 'Treatment Effectiveness'),
        ('regional_analysis', 'Regional Analysis'),
        ('seasonal_patterns', 'Seasonal Patterns'),
    ]

    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPES)
    description = models.TextField(blank=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report_data = models.JSONField(default=dict)
    date_range_start = models.DateField()
    date_range_end = models.DateField()
    filters_applied = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_report_type_display()}"

    class Meta:
        ordering = ['-created_at']


class DiseaseStatistics(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    region = models.CharField(max_length=100, blank=True)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    occurrence_count = models.PositiveIntegerField(default=0)
    severity_average = models.FloatField(default=0.0)
    treatment_success_rate = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['disease', 'crop', 'region', 'month', 'year']
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.disease.name} in {self.crop.name} - {self.month}/{self.year}"


class UserActivityLog(models.Model):
    ACTIVITY_TYPES = [
        ('diagnosis_request', 'Diagnosis Request'),
        ('treatment_started', 'Treatment Started'),
        ('treatment_completed', 'Treatment Completed'),
        ('feedback_submitted', 'Feedback Submitted'),
        ('report_generated', 'Report Generated'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=25, choices=ACTIVITY_TYPES)
    details = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_activity_type_display()}"

    class Meta:
        ordering = ['-timestamp']


class RegionalData(models.Model):
    region_name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100, blank=True)
    climate_type = models.CharField(max_length=50, blank=True)
    primary_crops = models.ManyToManyField(Crop, related_name='primary_regions')
    total_users = models.PositiveIntegerField(default=0)
    total_diagnoses = models.PositiveIntegerField(default=0)
    coordinates = models.CharField(max_length=50, blank=True, help_text="lat,lng")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.region_name}, {self.country}"

    class Meta:
        ordering = ['country', 'region_name']


class TrendAnalysis(models.Model):
    TREND_TYPES = [
        ('disease_outbreak', 'Disease Outbreak'),
        ('treatment_success', 'Treatment Success'),
        ('crop_yield', 'Crop Yield'),
        ('user_engagement', 'User Engagement'),
    ]

    trend_type = models.CharField(max_length=20, choices=TREND_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    trend_data = models.JSONField(default=dict)
    start_date = models.DateField()
    end_date = models.DateField()
    significance_score = models.FloatField(default=0.0, help_text="0-1 scale")
    regions_affected = models.ManyToManyField(RegionalData, blank=True)
    crops_affected = models.ManyToManyField(Crop, blank=True)
    diseases_involved = models.ManyToManyField(Disease, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_trend_type_display()})"

    class Meta:
        ordering = ['-significance_score', '-created_at']
