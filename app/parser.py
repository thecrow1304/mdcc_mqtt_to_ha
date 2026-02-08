from discovery import publish_entity
from utils import slugify
from config_store import config_store

def handle_message(topic, payload, mqtt):
    parts = topic.split("/")
    tenant = parts[4]
    device_type = parts[6]
    device_id = parts[7]

    device = f"{tenant}_{slugify(device_id)}"
    sensor = payload.get("sensor", {})
    message = payload.get("message", {})

    device_info = {
        "identifiers": [device],
        "name": sensor.get("alias", device),
        "model": device_type,
        "manufacturer": "physec"
    }

    for key, val in message.items():
        entity = slugify(key)

        if "valueNumber" in val:
            default_unit = val.get("unit")
            value = val["valueNumber"]
            domain = "sensor"
        elif "valueBoolean" in val:
            default_unit = None
            value = val["valueBoolean"]
            domain = "binary_sensor"
        else:
            default_unit = None
            value = val.get("value")
            domain = "sensor"

        config_store.register_entity(device, entity, {"unit": default_unit})
        cfg = config_store.get_entity(device, entity)

        if not cfg["enabled"]:
            continue

        publish_entity(
            mqtt,
            device,
            entity,
            value,
            domain,
            device_info,
            cfg
        )
