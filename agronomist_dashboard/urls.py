from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('disease-reports/', views.disease_reports, name='disease_reports'),
    path('iot-data/', views.iot_data, name='iot_data'),
    path('analytics/', views.analytics, name='analytics'),
    path('advisory/', views.advisory, name='advisory'),
]
# This file defines the URL patterns for the agronomist dashboard application.