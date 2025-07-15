from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'diagnosis' 

urlpatterns = [
    #path('',views.index, name='home'),
    path('', views.index, name='index'),  
    path('index/', views.index, name='index'),
    # path('get_recommendations/', views.get_recommendations, name='get_recommendations'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)