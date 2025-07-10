
from django.urls import path
from . import api_views

urlpatterns = [
    path('dashboard/', api_views.AnalyticsDashboardAPIView.as_view(), name='api_analytics_dashboard'),
    path('disease-trends/', api_views.DiseaseTrendsAPIView.as_view(), name='api_disease_trends'),
    path('regional-data/', api_views.RegionalDataAPIView.as_view(), name='api_regional_data'),
    path('user-activity/', api_views.UserActivityAPIView.as_view(), name='api_user_activity'),
]
