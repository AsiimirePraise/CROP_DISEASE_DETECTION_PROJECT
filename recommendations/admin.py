
from django.contrib import admin
from .models import (
    TreatmentCategory, Treatment, Recommendation, TreatmentRecommendation,
    TreatmentTracking, PreventiveMeasure
)


@admin.register(TreatmentCategory)
class TreatmentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'treatment_type', 'effectiveness_rating', 'organic_friendly']
    list_filter = ['treatment_type', 'organic_friendly', 'category']
    search_fields = ['name', 'active_ingredients']
    filter_horizontal = ['diseases']


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['diagnosis_result', 'priority_level', 'estimated_cost', 'follow_up_required', 'created_at']
    list_filter = ['priority_level', 'follow_up_required', 'created_at']
    filter_horizontal = ['treatments']


@admin.register(TreatmentRecommendation)
class TreatmentRecommendationAdmin(admin.ModelAdmin):
    list_display = ['recommendation', 'treatment', 'order', 'quantity_needed']
    list_filter = ['order']


@admin.register(TreatmentTracking)
class TreatmentTrackingAdmin(admin.ModelAdmin):
    list_display = ['user', 'treatment', 'status', 'effectiveness_rating', 'start_date', 'completion_date']
    list_filter = ['status', 'effectiveness_rating', 'start_date']
    search_fields = ['user__email', 'treatment__name']


@admin.register(PreventiveMeasure)
class PreventiveMeasureAdmin(admin.ModelAdmin):
    list_display = ['name', 'implementation_cost', 'difficulty_level', 'effectiveness']
    list_filter = ['implementation_cost', 'difficulty_level']
    search_fields = ['name', 'description']
    filter_horizontal = ['diseases']
