from django.contrib import admin
from .models import SensorType, SensorData, ProjectLink


@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'mqtt_topic', 'unit', 'created_at')
    search_fields = ('name', 'mqtt_topic')
    readonly_fields = ('created_at',)


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'value', 'timestamp')
    list_filter = ('sensor', 'timestamp')
    search_fields = ('sensor__name',)
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)


@admin.register(ProjectLink)
class ProjectLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at',)
