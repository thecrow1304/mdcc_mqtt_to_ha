import threading
from fastapi import FastAPI
import uvicorn

from mqtt_client import start_mqtt
from panel import router as panel_router
from panel_api import router as api_router

app = FastAPI(title="IoTree MQTT Auto Discovery v2")

app.include_router(panel_router)
app.include_router(api_router)

if __name__ == "__main__":
    threading.Thread(target=start_mqtt, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8099)
