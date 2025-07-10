
from rest_framework import serializers
from .models import DiagnosisRequest, DiagnosisResult, Crop, Disease, DiseaseDetection


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ['id', 'name', 'scientific_name', 'category', 'growing_season']


class DiseaseSerializer(serializers.ModelSerializer):
    crops = CropSerializer(many=True, read_only=True)

    class Meta:
        model = Disease
        fields = [
            'id', 'name', 'scientific_name', 'severity', 'symptoms',
            'causes', 'prevention_methods', 'treatment_methods', 'crops'
        ]


class DiseaseDetectionSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer(read_only=True)

    class Meta:
        model = DiseaseDetection
        fields = [
            'disease', 'confidence_score', 'affected_area_percentage',
            'severity_assessment'
        ]


class DiagnosisResultSerializer(serializers.ModelSerializer):
    detected_diseases = DiseaseDetectionSerializer(
        source='diseasedetection_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = DiagnosisResult
        fields = [
            'overall_health_status', 'recommendations', 'urgency_level',
            'detected_diseases', 'created_at'
        ]


class DiagnosisRequestSerializer(serializers.ModelSerializer):
    result = DiagnosisResultSerializer(read_only=True)
    crop = CropSerializer(read_only=True)

    class Meta:
        model = DiagnosisRequest
        fields = [
            'id', 'crop', 'image', 'location', 'gps_coordinates',
            'description', 'status', 'confidence_score', 'processing_time',
            'created_at', 'result'
        ]
        read_only_fields = ['id', 'status', 'confidence_score', 'processing_time', 'created_at']


class DiagnosisUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisRequest
        fields = ['crop', 'image', 'location', 'gps_coordinates', 'description']
