
from django.urls import path
from . import api_views

urlpatterns = [
    path('upload/', api_views.DiagnosisUploadAPIView.as_view(), name='api_diagnosis_upload'),
    path('results/<uuid:diagnosis_id>/', api_views.DiagnosisResultAPIView.as_view(), name='api_diagnosis_result'),
    path('crops/', api_views.CropListAPIView.as_view(), name='api_crops'),
    path('diseases/', api_views.DiseaseListAPIView.as_view(), name='api_diseases'),
]
