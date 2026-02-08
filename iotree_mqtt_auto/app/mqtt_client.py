import json
import ssl
import time
import logging
import paho.mqtt.client as mqtt

LOG = logging.getLogger("mqtt_client")
logging.basicConfig(level=logging.INFO)


# -------------------------------------------------
# Load Home Assistant Add-on options
# -------------------------------------------------
def load_options():
    try:
        with open("/data/options.json", "r") as f:
            return json.load(f)
    except Exception as e:
        LOG.error("Failed to load /data/options.json: %s", e)
        raise


# -------------------------------------------------
# MQTT Callbacks
# -------------------------------------------------
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        LOG.info("MQTT connected successfully")

        topic = userdata.get("mqtt_topic")
        if topic:
            client.subscribe(topic)
            LOG.info("Subscribed to %s", topic)

    else:
        LOG.error("MQTT connection failed with code %s", rc)


def on_disconnect(client, userdata, rc, properties=None):
    LOG.warning("MQTT disconnected (rc=%s)", rc)


def on_message(client, userdata, msg):
    LOG.info("MQTT Message %s -> %s", msg.topic, msg.payload.decode(errors="ignore"))


# -------------------------------------------------
# MQTT Setup
# -------------------------------------------------
def create_client(options):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=options)

    # Username / Password
    if options.get("mqtt_username"):
        client.username_pw_set(
            options.get("mqtt_username"),
            options.get("mqtt_password", "")
        )

    # TLS if needed
    if int(options.get("mqtt_port", 1883)) == 8883:
        LOG.info("Enabling TLS for MQTT connection")
        client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
        client.tls_insecure_set(False)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    return client


# -------------------------------------------------
# Connect with retry
# -------------------------------------------------
def connect_loop(client, options):
    host = options.get("mqtt_host")
    port = int(options.get("mqtt_port", 1883))

    while True:
        try:
            LOG.info("Connecting to MQTT %s:%s", host, port)
            client.connect(host, port, keepalive=60)
            return
        except Exception as e:
            LOG.error("MQTT connect failed: %s", e)
            time.sleep(5)


# -------------------------------------------------
# Main entry
# -------------------------------------------------
def start_mqtt():
    options = load_options()

    client = create_client(options)

    connect_loop(client, options)

    client.loop_forever()


# -------------------------------------------------
# Run directly
# -------------------------------------------------
if __name__ == "__main__":
    start_mqtt()
