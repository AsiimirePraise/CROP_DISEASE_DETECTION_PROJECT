
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_dashboard_view, name='dashboard'),
    path('reports/', views.reports_list_view, name='reports'),
    path('reports/generate/', views.generate_report_view, name='generate_report'),
    path('reports/<int:report_id>/', views.report_detail_view, name='report_detail'),
    path('trends/', views.trends_view, name='trends'),
    path('regional/', views.regional_analysis_view, name='regional'),
]
