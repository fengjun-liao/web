from django.urls import path

from . import views

urlpatterns = [
    path('/member2/', views.index, name='index'),
    path('/member2/about/', views.about, name='about'),
    path('/member2/dashboard/', views.sensor_dashboard, name='dashboard'),
    path('/member2/sensor/<int:sensor_id>/', views.sensor_detail, name='sensor_detail'),
    path('/member2/api/sensor/<int:sensor_id>/data/', views.sensor_data_api, name='sensor_data_api'),
    path('/member2/api/chart-history/', views.chart_history_api, name='chart_history_api'),
    path('/member2/raw-data/', views.raw_data_view, name='raw_data'),
    path('projects/', views.projects, name='projects'),
]
