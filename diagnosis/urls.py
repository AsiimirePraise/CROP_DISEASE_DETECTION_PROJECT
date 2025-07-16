from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'diagnosis' 

urlpatterns = [
    path('',views.index, name='home'),

    path('index', views.index, name='index'),      #this is the one for the farmer's dashboard
    
    path('reportIssue/', views.reportIssue, name='reportIssue'),
    
    # path('get_recommendations/', views.get_recommendations, name='get_recommendations'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)