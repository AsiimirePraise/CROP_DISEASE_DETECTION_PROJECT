
from django.urls import path
from . import api_views

urlpatterns = [
    path('profile/', api_views.UserProfileAPIView.as_view(), name='api_user_profile'),
    path('dashboard-stats/', api_views.DashboardStatsAPIView.as_view(), name='api_dashboard_stats'),
]
