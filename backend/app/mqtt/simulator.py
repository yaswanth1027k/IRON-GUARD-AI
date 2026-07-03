import asyncio
import json

import random
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

# Configuration for the local MQTT broker running in Docker
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_BASE = "ironguard/sensors"

# Create an MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "SensorSimulator")

def generate_sensor_data(sensor_id, sensor_type):
    """Generates realistic dummy data based on the sensor type"""
    data = {
        "sensor_id": sensor_id,
        "type": sensor_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "unit": "",
        "value": 0.0,
        "status": "OK"
    }

    if sensor_type == "gas":
        data["value"] = round(random.uniform(0.0, 50.0), 2) # ppm
        data["unit"] = "ppm"
        if data["value"] > 40.0:
            data["status"] = "WARNING"
            
    elif sensor_type == "temperature":
        data["value"] = round(random.uniform(20.0, 100.0), 2) # Celsius
        data["unit"] = "C"
        if data["value"] > 85.0:
            data["status"] = "WARNING"

    return data

async def run_simulator():
    print(f"Connecting to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}...")
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        print("Connected! Starting telemetry broadcast...")
    except Exception as e:
        print(f"Failed to connect to MQTT: {e}")
        return

    # Simulate 3 different sensors
    sensors = [
        {"id": 1, "type": "gas"},
        {"id": 2, "type": "temperature"},
        {"id": 3, "type": "gas"}
    ]

    try:
        while True:
            for sensor in sensors:
                payload = generate_sensor_data(sensor["id"], sensor["type"])
                topic = f"{TOPIC_BASE}/{sensor['type']}/{sensor['id']}"
                
                # Publish the JSON payload to the MQTT broker
                client.publish(topic, json.dumps(payload))
                print(f"Published to {topic}: {payload['value']} {payload['unit']}")
            
            # Wait 2 seconds before the next reading
            await asyncio.sleep(2)
            
    except KeyboardInterrupt:
        print("Stopping simulator...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    # Ensure paho-mqtt is installed: pip install paho-mqtt
    asyncio.run(run_simulator())