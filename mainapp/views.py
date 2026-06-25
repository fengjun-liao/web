import json
import random
from datetime import timedelta

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import SensorType, SensorData, ProjectLink


# Personal information
PERSONAL_INFO = {
    "name": "廖烽均",
    "student_id": "B11213032",
}


def index(request):
    """Render the personal website home page."""
    # Get latest sensor readings
    sensors = SensorType.objects.all()
    latest_readings = {}
    
    for sensor in sensors:
        latest = sensor.readings.first()
        if latest:
            latest_readings[sensor.id] = {
                'name': sensor.name,
                'value': latest.value,
                'unit': sensor.unit,
                'timestamp': latest.timestamp,
                'mqtt_topic': sensor.mqtt_topic,
            }
    
    # Get project links
    project_links = ProjectLink.objects.all()
    
    context = {
        "title": "廖烽均 - 個人網站",
        "heading": "感測器資料監測系統",
        "message": "即時顯示MQTT感測器資料，並儲存到資料庫。",
        "name": PERSONAL_INFO['name'],
        "student_id": PERSONAL_INFO['student_id'],
        "latest_readings": latest_readings,
        "sensors_count": sensors.count(),
        "project_links": project_links,
    }
    return render(request, "mainapp/index.html", context)


def about(request):
    """Render a simple about page."""
    context = {
        "title": "About This Site",
        "heading": "About the Personal Website",
        "message": "This site displays real-time sensor data from MQTT topics with historical charts.",
        "name": PERSONAL_INFO['name'],
        "student_id": PERSONAL_INFO['student_id'],
    }
    return render(request, "mainapp/about.html", context)


def sensor_dashboard(request):
    """Display all sensors and their latest data"""
    sensors = SensorType.objects.all().prefetch_related('readings')
    
    sensor_data = []
    for sensor in sensors:
        latest = sensor.readings.first()
        data_count = sensor.readings.count()
        
        sensor_data.append({
            'id': sensor.id,
            'name': sensor.name,
            'mqtt_topic': sensor.mqtt_topic,
            'unit': sensor.unit,
            'description': sensor.description,
            'latest_value': latest.value if latest else None,
            'latest_timestamp': latest.timestamp if latest else None,
            'total_readings': data_count,
        })
    
    context = {
        'sensors': sensor_data,
        'name': PERSONAL_INFO['name'],
        'student_id': PERSONAL_INFO['student_id'],
    }
    
    return render(request, 'mainapp/dashboard.html', context)


def sensor_detail(request, sensor_id):
    """Display detailed view of a specific sensor"""
    try:
        sensor = SensorType.objects.get(id=sensor_id)
    except SensorType.DoesNotExist:
        context = {
            'error': 'Sensor not found',
            'name': PERSONAL_INFO['name'],
            'student_id': PERSONAL_INFO['student_id'],
        }
        return render(request, 'mainapp/error.html', context, status=404)
    
    # Get data for the last 24 hours by default
    days = int(request.GET.get('days', 1))
    time_threshold = timezone.now() - timedelta(days=days)
    
    readings = sensor.readings.filter(timestamp__gte=time_threshold).order_by('timestamp')
    
    context = {
        'sensor': sensor,
        'readings': readings,
        'days': days,
        'readings_count': readings.count(),
        'name': PERSONAL_INFO['name'],
        'student_id': PERSONAL_INFO['student_id'],
    }
    
    return render(request, 'mainapp/sensor_detail.html', context)


@require_http_methods(["GET"])
def sensor_data_api(request, sensor_id):
    """API endpoint to get sensor data in JSON format for charts"""
    try:
        sensor = SensorType.objects.get(id=sensor_id)
    except SensorType.DoesNotExist:
        return JsonResponse({'error': 'Sensor not found'}, status=404)
    
    # Get data for the requested time period
    days = int(request.GET.get('days', 1))
    time_threshold = timezone.now() - timedelta(days=days)
    
    readings = sensor.readings.filter(timestamp__gte=time_threshold).order_by('timestamp')
    
    data = {
        'sensor': {
            'id': sensor.id,
            'name': sensor.name,
            'unit': sensor.unit,
            'mqtt_topic': sensor.mqtt_topic,
        },
        'timestamps': [r.timestamp.isoformat() for r in readings],
        'values': [r.value for r in readings],
        'min': min(r.value for r in readings) if readings else None,
        'max': max(r.value for r in readings) if readings else None,
        'avg': sum(r.value for r in readings) / len(readings) if readings else None,
        'count': len(readings),
    }
    
    return JsonResponse(data)


def raw_data_view(request):
    """View for browsing all raw sensor data with filtering"""
    sensor_id = request.GET.get('sensor')
    days = int(request.GET.get('days', 7))
    
    sensors = SensorType.objects.all()
    time_threshold = timezone.now() - timedelta(days=days)
    
    if sensor_id:
        try:
            selected_sensor = SensorType.objects.get(id=sensor_id)
            readings = SensorData.objects.filter(
                sensor=selected_sensor,
                timestamp__gte=time_threshold
            ).order_by('-timestamp')[:1000]  # Limit to 1000 entries
        except SensorType.DoesNotExist:
            selected_sensor = None
            readings = []
    else:
        selected_sensor = None
        readings = SensorData.objects.filter(
            timestamp__gte=time_threshold
        ).order_by('-timestamp')[:1000]
    
    context = {
        'readings': readings,
        'sensors': sensors,
        'selected_sensor': selected_sensor,
        'days': days,
        'name': PERSONAL_INFO['name'],
        'student_id': PERSONAL_INFO['student_id'],
    }
    
    return render(request, 'mainapp/raw_data.html', context)


def projects(request):
    """Display project links"""
    project_links = ProjectLink.objects.all()
    
    context = {
        'project_links': project_links,
        'name': PERSONAL_INFO['name'],
        'student_id': PERSONAL_INFO['student_id'],
    }
    
    return render(request, 'mainapp/projects.html', context)


@require_http_methods(["GET"])
def chart_history_api(request):
    """API endpoint to get all sensors' history data for charts in JSON format"""
    # Get data for the last N days
    days = int(request.GET.get('days', 1))
    time_threshold = timezone.now() - timedelta(days=days)
    
    # Define sensor names to fetch
    sensor_names = ['水位', '濕度1', '濕度2', '濕度3']
    
    # Prepare response data
    timestamps = set()
    sensor_data = {}
    
    for name in sensor_names:
        try:
            sensor = SensorType.objects.get(name=name)
            readings = sensor.readings.filter(timestamp__gte=time_threshold).order_by('timestamp')
            
            sensor_data[name] = {
                'values': [{'timestamp': r.timestamp.isoformat(), 'value': r.value} for r in readings],
                'unit': sensor.unit,
            }
            
            # Collect all timestamps
            for r in readings:
                timestamps.add(r.timestamp.isoformat())
        except SensorType.DoesNotExist:
            sensor_data[name] = {'values': [], 'unit': ''}
    
    # Sort timestamps
    timestamps = sorted(list(timestamps))
    
    # Prepare data in the format Chart.js expects
    data = {
        'timestamps': timestamps,
        'sensors': sensor_data,
    }
    
    return JsonResponse(data)
