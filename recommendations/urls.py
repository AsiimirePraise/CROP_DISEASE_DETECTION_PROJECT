
from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    #path('', views.recommendation_list_view, name='list'),
   # path('<int:recommendation_id>/', views.recommendation_detail_view, name='detail'),
   # path('<int:recommendation_id>/track/', views.treatment_tracking_view, name='track'),
   # path('treatments/', views.treatment_list_view, name='treatments'),
   # path('treatments/<int:treatment_id>/', views.treatment_detail_view, name='treatment_detail'),
   # path('preventive/', views.preventive_measures_view, name='preventive'),
    path('weather/', views.get_weather_data, name='get_weather_data'),

]
