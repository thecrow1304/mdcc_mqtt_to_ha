import json

def publish_entity(mqtt, device, entity, value, domain, device_info, cfg):
    config_topic = f"homeassistant/{domain}/{device}/{entity}/config"
    state_topic = f"addon/iotree/state/{device}/{entity}"

    payload = {
        "name": cfg["name"],
        "state_topic": state_topic,
        "unique_id": f"{device}_{entity}",
        "device": device_info
    }

    if cfg.get("unit"):
        payload["unit_of_measurement"] = cfg["unit"]

    if cfg.get("device_class"):
        payload["device_class"] = cfg["device_class"]

    if cfg.get("state_class"):
        payload["state_class"] = cfg["state_class"]

    mqtt.publish(config_topic, json.dumps(payload), retain=True)
    mqtt.publish(state_topic, value, retain=True)
