from fastapi import APIRouter
from config_store import config_store

router = APIRouter(prefix="/api")

@router.get("/config")
def get_config():
    return config_store.all()

@router.post("/config/{device}/{entity}")
def update_entity(device: str, entity: str, data: dict):
    cfg = config_store.data[device][entity]
    cfg.update(data)
    config_store.save()
    return {"status": "ok"}