from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
    path('drones/', views.drones_list, name='drones'),
    path('forfaits/', views.forfaits_list, name='forfaits'),
    path('api/changer-photo-drone/', views.changer_photo_drone_ajax, name='changer_photo_drone'),
]
