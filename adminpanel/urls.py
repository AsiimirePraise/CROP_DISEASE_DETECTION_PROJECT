from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin_dashboard, name='admin-dashboard'),
    path('users/', views.manage_users, name='manage-users'),
    path('issues/', views.manage_issues, name='manage-issues'),
    path('datasets/', views.manage_datasets, name='manage-datasets'),
    path('retrain/', views.retrain_model, name='retrain-model'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit-user'),
    path('verify-upload/<int:upload_id>/', views.verify_upload, name='verify_upload'),
    path('upload-training-image/', views.upload_training_image, name='upload_training_image'),
    path('export-farmer-uploads/', views.export_to_csv, name='export_farmer_uploads'),
    path('export-training-images/', views.export_training_images, name='export_training_images'),
    path('issues/<int:issue_id>/edit/', views.edit_issue, name='edit_issue'),
]
