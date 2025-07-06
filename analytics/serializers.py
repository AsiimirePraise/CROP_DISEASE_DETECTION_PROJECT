
from rest_framework import serializers
from .models import AnalyticsReport, DiseaseStatistics, TrendAnalysis, RegionalData


class DiseaseStatisticsSerializer(serializers.ModelSerializer):
    disease_name = serializers.CharField(source='disease.name', read_only=True)
    crop_name = serializers.CharField(source='crop.name', read_only=True)

    class Meta:
        model = DiseaseStatistics
        fields = [
            'disease_name', 'crop_name', 'region', 'month', 'year',
            'occurrence_count', 'severity_average', 'treatment_success_rate'
        ]


class TrendAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendAnalysis
        fields = [
            'trend_type', 'title', 'description', 'trend_data',
            'start_date', 'end_date', 'significance_score', 'created_at'
        ]


class RegionalDataSerializer(serializers.ModelSerializer):
    primary_crops = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = RegionalData
        fields = [
            'region_name', 'country', 'state_province', 'climate_type',
            'primary_crops', 'total_users', 'total_diagnoses', 'coordinates'
        ]


class AnalyticsReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsReport
        fields = [
            'id', 'name', 'report_type', 'description', 'report_data',
            'date_range_start', 'date_range_end', 'filters_applied', 'created_at'
        ]
