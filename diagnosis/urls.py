
from django.urls import path
from . import views

app_name = 'diagnosis'

urlpatterns = [
    path('', views.diagnosis_list_view, name='list'),
    path('new/', views.diagnosis_create_view, name='create'),
    path('<uuid:diagnosis_id>/', views.diagnosis_detail_view, name='detail'),
    path('<uuid:diagnosis_id>/feedback/', views.feedback_create_view, name='feedback'),
    path('crops/', views.crop_list_view, name='crops'),
    path('diseases/', views.disease_list_view, name='diseases'),
    path('diseases/<int:disease_id>/', views.disease_detail_view, name='disease_detail'),
]
