from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Crop, Disease, Field, Diagnosis, SensorReading, TreatmentRecommendation


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name', 'created_at']
    search_fields = ['name', 'scientific_name']


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'severity', 'created_at']
    list_filter = ['severity']
    search_fields = ['name']
    filter_horizontal = ['affected_crops']


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'crop', 'area_hectares', 'created_at']
    list_filter = ['crop']
    search_fields = ['name', 'location']


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ['field', 'disease', 'severity', 'confidence', 'diagnosed_at']
    list_filter = ['severity', 'disease', 'diagnosed_at']
    search_fields = ['field__name', 'disease__name']
    date_hierarchy = 'diagnosed_at'


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ['field', 'sensor_type', 'value', 'unit', 'recorded_at']
    list_filter = ['sensor_type', 'field']
    search_fields = ['field__name']
    date_hierarchy = 'recorded_at'


@admin.register(TreatmentRecommendation)
class TreatmentRecommendationAdmin(admin.ModelAdmin):
    list_display = ['diagnosis', 'status', 'recommended_by', 'estimated_cost', 'created_at']
    list_filter = ['status']
    search_fields = ['diagnosis__field__name', 'diagnosis__disease__name']
    date_hierarchy = 'created_at'