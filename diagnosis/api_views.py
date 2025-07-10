
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import DiagnosisRequest, Crop, Disease
from .serializers import (
    DiagnosisUploadSerializer, DiagnosisRequestSerializer,
    CropSerializer, DiseaseSerializer
)
from .tasks import process_diagnosis


class DiagnosisUploadAPIView(generics.CreateAPIView):
    serializer_class = DiagnosisUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        diagnosis = serializer.save(user=self.request.user)
        # Trigger async processing
        process_diagnosis.delay(str(diagnosis.id))


class DiagnosisResultAPIView(generics.RetrieveAPIView):
    serializer_class = DiagnosisRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'diagnosis_id'

    def get_queryset(self):
        return DiagnosisRequest.objects.filter(user=self.request.user)


class CropListAPIView(generics.ListAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.IsAuthenticated]


class DiseaseListAPIView(generics.ListAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        severity = self.request.query_params.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
        return queryset
