"""
Django management command to listen to MQTT topics and store sensor data
Usage: python manage.py mqtt_listener
"""

import json
import logging
import time
from django.core.management.base import BaseCommand
from django.utils import timezone

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None

from mainapp.models import SensorType, SensorData

logger = logging.getLogger(__name__)


class MQTTClient:
    """MQTT client for listening to sensor topics"""
    
    def __init__(self, broker_host='localhost', broker_port=1883, username=None, password=None):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.client = None
        self.connected = False
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback when MQTT client connects"""
        if rc == 0:
            self.connected = True
            logger.info("MQTT connected successfully")
            # Subscribe to all sensor topics
            self.subscribe_to_sensors()
        else:
            logger.error(f"MQTT connection failed with code {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        """Callback when MQTT client disconnects"""
        self.connected = False
        if rc != 0:
            logger.warning(f"Unexpected MQTT disconnection: {rc}")
    
    def on_message(self, client, userdata, msg):
        """Callback when a message is received"""
        try:
            topic = msg.topic
            payload = msg.payload.decode()
            
            logger.debug(f"Received message on {topic}: {payload}")
            
            # Try to find or create sensor type for this topic
            sensor_type, created = SensorType.objects.get_or_create(mqtt_topic=topic)
            
            if created:
                sensor_type.name = topic.replace('/', '_')
                sensor_type.save()
                logger.info(f"Created new sensor type: {sensor_type.name}")
            
            # Parse the payload and store the data
            try:
                # Try to parse as JSON
                data = json.loads(payload)
                if isinstance(data, dict):
                    # If JSON object, try to extract a numeric value
                    value = data.get('value') or data.get('data') or list(data.values())[0]
                else:
                    value = float(data)
            except (json.JSONDecodeError, ValueError, TypeError):
                # Try direct float conversion
                value = float(payload)
            
            # Store the sensor data
            SensorData.objects.create(sensor=sensor_type, value=value)
            logger.info(f"Stored data for {sensor_type.name}: {value}")
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
    
    def subscribe_to_sensors(self):
        """Subscribe to all configured sensor topics"""
        sensors = SensorType.objects.all()
        for sensor in sensors:
            if sensor.mqtt_topic:
                self.client.subscribe(sensor.mqtt_topic)
                logger.info(f"Subscribed to {sensor.mqtt_topic}")
        
        # Also subscribe to a wildcard for discovering new topics
        self.client.subscribe('sensor/#')
        logger.info("Subscribed to sensor/# for auto-discovery")
    
    def connect(self):
        """Connect to MQTT broker"""
        if mqtt is None:
            raise ImportError("paho-mqtt is not installed. Run: pip install paho-mqtt")
        
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
        
        logger.info(f"Connecting to MQTT broker at {self.broker_host}:{self.broker_port}")
        self.client.connect(self.broker_host, self.broker_port, keepalive=60)
    
    def start_loop(self):
        """Start the MQTT client loop"""
        self.client.loop_start()
    
    def stop_loop(self):
        """Stop the MQTT client loop"""
        self.client.loop_stop()
        self.client.disconnect()


class Command(BaseCommand):
    help = 'Start listening to MQTT topics for sensor data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--broker',
            type=str,
            default='localhost',
            help='MQTT broker host (default: localhost)',
        )
        parser.add_argument(
            '--port',
            type=int,
            default=1883,
            help='MQTT broker port (default: 1883)',
        )
        parser.add_argument(
            '--username',
            type=str,
            default=None,
            help='MQTT username (optional)',
        )
        parser.add_argument(
            '--password',
            type=str,
            default=None,
            help='MQTT password (optional)',
        )
    
    def handle(self, *args, **options):
        if mqtt is None:
            self.stdout.write(
                self.style.ERROR(
                    'paho-mqtt is not installed. Install it with: pip install paho-mqtt'
                )
            )
            return
        
        self.stdout.write(self.style.SUCCESS('Starting MQTT listener...'))
        
        try:
            mqtt_client = MQTTClient(
                broker_host=options['broker'],
                broker_port=options['port'],
                username=options['username'],
                password=options['password'],
            )
            mqtt_client.connect()
            mqtt_client.start_loop()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Connected to MQTT broker at {options['broker']}:{options['port']}"
                )
            )
            self.stdout.write(
                self.style.SUCCESS('Listening for messages... Press Ctrl+C to stop.')
            )
            
            # Keep the command running
            while True:
                time.sleep(1)
        
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nStopping MQTT listener...'))
            mqtt_client.stop_loop()
            self.stdout.write(self.style.SUCCESS('MQTT listener stopped.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
