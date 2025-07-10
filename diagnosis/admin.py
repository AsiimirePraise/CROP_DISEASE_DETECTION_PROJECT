
from django.contrib import admin
from .models import Crop, Disease, DiagnosisRequest, DiagnosisResult, DiseaseDetection, FeedbackRating


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name', 'category', 'growing_season']
    search_fields = ['name', 'scientific_name']
    list_filter = ['category']


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'severity', 'created_at']
    list_filter = ['severity', 'created_at']
    search_fields = ['name', 'scientific_name']
    filter_horizontal = ['crops']


@admin.register(DiagnosisRequest)
class DiagnosisRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'crop', 'status', 'confidence_score', 'created_at']
    list_filter = ['status', 'crop', 'created_at']
    search_fields = ['user__email', 'crop__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(DiagnosisResult)
class DiagnosisResultAdmin(admin.ModelAdmin):
    list_display = ['diagnosis_request', 'overall_health_status', 'urgency_level', 'created_at']
    list_filter = ['overall_health_status', 'urgency_level', 'created_at']
    filter_horizontal = ['detected_diseases']


@admin.register(DiseaseDetection)
class DiseaseDetectionAdmin(admin.ModelAdmin):
    list_display = ['disease', 'confidence_score', 'severity_assessment', 'affected_area_percentage']
    list_filter = ['severity_assessment', 'disease']


@admin.register(FeedbackRating)
class FeedbackRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'accuracy_rating', 'usefulness_rating', 'would_recommend', 'created_at']
    list_filter = ['accuracy_rating', 'usefulness_rating', 'would_recommend', 'created_at']
    search_fields = ['user__email', 'comments']
