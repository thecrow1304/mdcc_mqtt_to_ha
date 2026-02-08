import json
import paho.mqtt.client as mqtt
from parser import handle_message

MQTT_TOPIC = "physec/iotree-+/iot-platform/+/sensor/+/+"

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        handle_message(msg.topic, payload, client)
    except Exception as e:
        print("MQTT error:", e)

def start_mqtt():
    client = mqtt.Client()
    client.connect("core-mosquitto", 1883)
    client.subscribe(MQTT_TOPIC)
    client.on_message = on_message
    client.loop_forever()
