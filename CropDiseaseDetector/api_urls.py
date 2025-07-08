
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.api_urls')),
    path('diagnosis/', include('diagnosis.api_urls')),
    path('recommendations/', include('recommendations.api_urls')),
    path('analytics/', include('analytics.api_urls')),

]
