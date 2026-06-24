#!/usr/bin/env python
"""
Utility script for managing the personal website.

This script provides various management commands for the website.
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
sys.path.insert(0, str(Path(__file__).parent))
django.setup()

from mainapp.models import SensorType, SensorData, ProjectLink


def list_sensors():
    """List all configured sensors."""
    print("\n=== Configured Sensors ===")
    sensors = SensorType.objects.all()
    if not sensors:
        print("No sensors configured.")
        return
    
    for sensor in sensors:
        latest = sensor.readings.first()
        print(f"\n- {sensor.name}")
        print(f"  MQTT Topic: {sensor.mqtt_topic}")
        print(f"  Unit: {sensor.unit or 'N/A'}")
        print(f"  Total Readings: {sensor.readings.count()}")
        if latest:
            print(f"  Latest Value: {latest.value} (at {latest.timestamp})")


def list_projects():
    """List all configured project links."""
    print("\n=== Project Links ===")
    projects = ProjectLink.objects.all()
    if not projects:
        print("No project links configured.")
        return
    
    for project in projects:
        print(f"\n- {project.title}")
        print(f"  URL: {project.url}")
        if project.description:
            print(f"  Description: {project.description}")


def add_sensor(name, mqtt_topic, unit="", description=""):
    """Add a new sensor."""
    sensor, created = SensorType.objects.get_or_create(
        mqtt_topic=mqtt_topic,
        defaults={
            'name': name,
            'unit': unit,
            'description': description,
        }
    )
    if created:
        print(f"✓ Sensor '{sensor.name}' added successfully.")
    else:
        print(f"✗ Sensor with MQTT topic '{mqtt_topic}' already exists.")


def add_project(title, url, description=""):
    """Add a new project link."""
    project = ProjectLink.objects.create(
        title=title,
        url=url,
        description=description,
    )
    print(f"✓ Project '{project.title}' added successfully.")


def sample_data():
    """Create sample sensors and projects for testing."""
    print("\n=== Creating Sample Data ===")
    
    # Sample sensors
    sensors_data = [
        ("Temperature Sensor", "sensor/temperature", "°C", "Room temperature monitoring"),
        ("Humidity Sensor", "sensor/humidity", "%", "Room humidity level"),
        ("CO2 Sensor", "sensor/co2", "ppm", "CO2 concentration"),
    ]
    
    for name, topic, unit, desc in sensors_data:
        add_sensor(name, topic, unit, desc)
    
    # Sample projects
    projects_data = [
        ("IoT Project", "https://github.com", "Smart home automation system"),
        ("Data Analysis", "https://example.com/analysis", "Historical data visualization"),
    ]
    
    for title, url, desc in projects_data:
        project, created = ProjectLink.objects.get_or_create(
            title=title,
            defaults={'url': url, 'description': desc}
        )
        if created:
            print(f"✓ Project '{title}' added successfully.")
        else:
            print(f"  Project '{title}' already exists.")


def clear_data():
    """Clear all sensor data (but keep sensor types and project links)."""
    count = SensorData.objects.all().delete()[0]
    print(f"✓ Deleted {count} sensor data records.")


def stats():
    """Display statistics."""
    print("\n=== Statistics ===")
    print(f"Total Sensors: {SensorType.objects.count()}")
    print(f"Total Readings: {SensorData.objects.count()}")
    print(f"Total Projects: {ProjectLink.objects.count()}")
    
    # Stats per sensor
    print("\nReadings per sensor:")
    for sensor in SensorType.objects.all():
        print(f"  - {sensor.name}: {sensor.readings.count()} readings")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""
Usage: python utils.py <command> [options]

Commands:
  list-sensors         List all configured sensors
  list-projects        List all configured project links
  add-sensor           Add a new sensor
  add-project          Add a new project link
  sample-data          Create sample sensors and projects
  clear-data           Clear all sensor data
  stats                Display statistics

Examples:
  python utils.py list-sensors
  python utils.py add-sensor "Temperature" "sensor/temp" "°C" "Temperature monitoring"
  python utils.py sample-data
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list-sensors':
        list_sensors()
    elif command == 'list-projects':
        list_projects()
    elif command == 'add-sensor':
        if len(sys.argv) < 4:
            print("Usage: python utils.py add-sensor <name> <mqtt_topic> [unit] [description]")
            sys.exit(1)
        add_sensor(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "", 
                   sys.argv[5] if len(sys.argv) > 5 else "")
    elif command == 'add-project':
        if len(sys.argv) < 4:
            print("Usage: python utils.py add-project <title> <url> [description]")
            sys.exit(1)
        add_project(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
    elif command == 'sample-data':
        sample_data()
    elif command == 'clear-data':
        confirm = input("Are you sure you want to clear all sensor data? (yes/no): ")
        if confirm.lower() == 'yes':
            clear_data()
        else:
            print("Cancelled.")
    elif command == 'stats':
        stats()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
