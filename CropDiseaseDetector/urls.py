
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('diagnosis/', include('diagnosis.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('analytics/', include('analytics.urls')),
    path('iot/', include('iot_integration.urls')),
    path('admin-panel/', include('admin_panel.urls')),
    path('api/', include('CropDiseaseDetector.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
