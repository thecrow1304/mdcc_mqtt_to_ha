import json
from pathlib import Path

CONFIG_FILE = Path("/data/config.json")

class ConfigStore:
    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        if CONFIG_FILE.exists():
            self.data = json.loads(CONFIG_FILE.read_text())
        else:
            self.data = {}

    def save(self):
        CONFIG_FILE.parent.mkdir(exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(self.data, indent=2))

    def register_entity(self, device, entity, defaults):
        self.data.setdefault(device, {})
        self.data[device].setdefault(entity, {
            "enabled": True,
            "name": entity,
            "unit": defaults.get("unit"),
            "device_class": None,
            "state_class": None
        })
        self.save()

    def get_entity(self, device, entity):
        return self.data.get(device, {}).get(entity)

    def all(self):
        return self.data

config_store = ConfigStore()
