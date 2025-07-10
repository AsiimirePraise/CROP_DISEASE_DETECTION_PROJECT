from django.urls import path
from .views import register, profile, home, dashboard, logout_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]
