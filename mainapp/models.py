from django.db import models
from django.utils import timezone


class SensorType(models.Model):
    """Model to store different types of sensors"""
    name = models.CharField(max_length=100, unique=True)
    mqtt_topic = models.CharField(max_length=200, unique=True)
    unit = models.CharField(max_length=50, default="")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Sensor Types"
    
    def __str__(self):
        return self.name


class SensorData(models.Model):
    """Model to store sensor readings"""
    sensor = models.ForeignKey(SensorType, on_delete=models.CASCADE, related_name='readings')
    value = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sensor', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.sensor.name}: {self.value} ({self.timestamp})"


class ProjectLink(models.Model):
    """Model to store links to group projects"""
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
