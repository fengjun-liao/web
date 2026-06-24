#!/usr/bin/env python
"""
Simple MQTT test client for sending test data to the sensor topics.

This is a utility script to help test the MQTT listener without needing actual sensors.

Usage:
    python mqtt_test_client.py --broker localhost --topic sensor/temperature --value 25.5
"""

import argparse
import time
import random
import sys

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("Error: paho-mqtt is not installed.")
    print("Install it with: pip install paho-mqtt")
    sys.exit(1)


class MQTTTestClient:
    """Simple MQTT client for testing."""
    
    def __init__(self, broker_host, broker_port=1883, username=None, password=None):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.client = None
        self.connected = False
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(f"✓ Connected to MQTT broker at {self.broker_host}:{self.broker_port}")
        else:
            print(f"✗ Failed to connect, return code {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        if rc != 0:
            print(f"Unexpected disconnection: {rc}")
    
    def connect(self):
        """Connect to MQTT broker."""
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
        
        self.client.connect(self.broker_host, self.broker_port, keepalive=60)
        self.client.loop_start()
        
        # Wait for connection
        timeout = 10
        start = time.time()
        while not self.connected and time.time() - start < timeout:
            time.sleep(0.1)
        
        if not self.connected:
            raise Exception("Failed to connect to MQTT broker")
    
    def publish(self, topic, payload):
        """Publish a message."""
        if not self.connected:
            print("✗ Not connected to MQTT broker")
            return False
        
        result = self.client.publish(topic, payload)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"✓ Published to {topic}: {payload}")
            return True
        else:
            print(f"✗ Failed to publish: {result.rc}")
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from MQTT broker")


def main():
    parser = argparse.ArgumentParser(
        description='MQTT test client for sending test data to sensor topics'
    )
    parser.add_argument('--broker', default='localhost', help='MQTT broker host')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port')
    parser.add_argument('--username', help='MQTT username')
    parser.add_argument('--password', help='MQTT password')
    parser.add_argument('--topic', required=True, help='MQTT topic to publish to')
    parser.add_argument('--value', required=True, help='Value to publish')
    parser.add_argument('--repeat', type=int, default=1, help='Number of times to publish')
    parser.add_argument('--interval', type=int, default=1, help='Interval between publishes (seconds)')
    parser.add_argument('--random', action='store_true', help='Generate random values')
    parser.add_argument('--random-range', nargs=2, type=float, default=[0, 100],
                        help='Range for random values (min max)')
    
    args = parser.parse_args()
    
    try:
        client = MQTTTestClient(args.broker, args.port, args.username, args.password)
        client.connect()
        
        for i in range(args.repeat):
            if args.random:
                value = random.uniform(args.random_range[0], args.random_range[1])
                payload = f"{value:.2f}"
            else:
                payload = args.value
            
            client.publish(args.topic, payload)
            
            if i < args.repeat - 1:
                time.sleep(args.interval)
        
        client.disconnect()
        print("\n✓ Test completed successfully")
    
    except KeyboardInterrupt:
        print("\n✗ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
