from django.urls import path
from . import views

app_name = 'diagnosis'  # This creates a namespace

urlpatterns = [
    #path('',views.index, name='home'),
    path('', views.index, name='index'),  # This handles localhost:8000/
    path('index/', views.index, name='index'),
]