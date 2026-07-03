import json
import logging
from typing import Any

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPICS = [("ironguard/sensors/#", 0)]

latest_readings: dict[str, dict[str, Any]] = {}


def on_connect(client: mqtt.Client, userdata, flags, rc, properties=None):
    logger.info("MQTT connected rc=%s", rc)
    for topic, qos in MQTT_TOPICS:
        client.subscribe(topic, qos=qos)
        logger.info("Subscribed to topic=%s qos=%s", topic, qos)


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        latest_readings[msg.topic] = payload
        logger.info("MQTT message topic=%s payload=%s", msg.topic, payload)
    except Exception as e:
        logger.exception("Failed to process MQTT message on %s: %s", msg.topic, e)


def create_mqtt_client() -> mqtt.Client:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="iron-guard-subscriber")
    client.on_connect = on_connect
    client.on_message = on_message
    return client