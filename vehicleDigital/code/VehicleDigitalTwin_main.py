import os
from dotenv import dotenv_values # Cargar variables de entorno
import threading
import json
import time
from tb_device_mqtt import TBDeviceMqttClient
from fastapi import FastAPI
import uvicorn


# Cargar variables de entorno desde el archivo .env_vars
env_vars = dotenv_values('/usr/src/app/.env_vars')

# Acceder a las variables de entorno cargadas
api_key = env_vars.get('API_KEY')
api_pass = env_vars.get('API_PASS')
token = env_vars.get('TOKEN')

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello, Mundo"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)