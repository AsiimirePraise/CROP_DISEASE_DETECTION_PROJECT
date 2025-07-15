from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin_dashboard, name='admin-dashboard'),
    path('users/', views.manage_users, name='manage-users'),
    path('issues/', views.manage_issues, name='manage-issues'),
    path('datasets/', views.manage_datasets, name='manage-datasets'),
    path('retrain/', views.retrain_model, name='retrain-model'),
     path('users/edit/<int:user_id>/', views.edit_user, name='edit-user'),
]
