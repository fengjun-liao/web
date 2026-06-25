from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.sensor_dashboard, name='dashboard'),
    path('sensor/<int:sensor_id>/', views.sensor_detail, name='sensor_detail'),
    path('api/sensor/<int:sensor_id>/data/', views.sensor_data_api, name='sensor_data_api'),
    path('raw-data/', views.raw_data_view, name='raw_data'),
    path('projects/', views.projects, name='projects'),
]
