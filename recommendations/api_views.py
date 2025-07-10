
from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Recommendation, Treatment, TreatmentTracking
from .serializers import RecommendationSerializer, TreatmentSerializer, TreatmentTrackingSerializer


class RecommendationListAPIView(generics.ListAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Recommendation.objects.filter(
            diagnosis_result__diagnosis_request__user=self.request.user
        )


class RecommendationDetailAPIView(generics.RetrieveAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'recommendation_id'

    def get_queryset(self):
        return Recommendation.objects.filter(
            diagnosis_result__diagnosis_request__user=self.request.user
        )


class TreatmentListAPIView(generics.ListAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class TreatmentTrackingAPIView(generics.ListCreateAPIView):
    serializer_class = TreatmentTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TreatmentTracking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
