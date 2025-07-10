
from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.RecommendationListAPIView.as_view(), name='api_recommendations'),
    path('<int:recommendation_id>/', api_views.RecommendationDetailAPIView.as_view(), name='api_recommendation_detail'),
    path('treatments/', api_views.TreatmentListAPIView.as_view(), name='api_treatments'),
    path('tracking/', api_views.TreatmentTrackingAPIView.as_view(), name='api_treatment_tracking'),
]
