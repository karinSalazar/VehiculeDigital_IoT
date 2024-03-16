import os
from dotenv import dotenv_values
from threading import Thread
import json
import time
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from fastapi import FastAPI
import uvicorn

# Cargamos las variables de entorno desde el archivo .env_vars
env_vars = dotenv_values('/usr/src/app/.env_vars')

# Accedemos a las variables de entorno cargadas
api_key = env_vars.get('API_KEY')
api_pass = env_vars.get('API_PASS')
token = env_vars.get('TOKEN')
broker = env_vars.get('BROKER3') 
port = 1883

app = FastAPI()


def es_mi_vehiculo(matricula):
    return matricula == "ABC123"

def obtener_id_vehiculo(matricula):
    vehiculos = {
        "ABC123": "vehiculo_1",
        "XYZ789": "Vehiculo2",
        # Otros vehículos...
    }
    return vehiculos.get(matricula, "Desconocido")

def routes_loader(vehicle_id, ruta):
    rutas_pendientes = {}
    print("Diccionario de rutas: ", rutas_pendientes)
    print("rutas: ", ruta)
    # Verificamos si ya hay rutas pendientes para este vehículo, si no hay rutas pendientes para este vehículo, crear una nueva lista de rutas
    if vehicle_id in rutas_pendientes:
        rutas_pendientes[vehicle_id].append(rutas_pendientes)
    else:        
        rutas_pendientes[vehicle_id] = [ruta]
    
    print("Ruta asignada al vehículo", vehicle_id, ": Origen:", ruta["Origen"], ", Destino:", ruta["Destino"])

def rpc_request_handler(client, request_id, request_body):
    print("Solicitud RPC recibida:", request_body)
    if request_body["method"] == "assignRoute":
        if "params" in request_body and "Origen" in request_body["params"] and "Destino" in request_body["params"]:
            # Verificamos si esta instancia es el vehículo al que va dirigido el comando (comparar el identificador matricula == "ABC123")
            matricula = request_body["params"]["Matricula"]
            vehicle_id = obtener_id_vehiculo(matricula)
            if vehicle_id != "Desconocido":
                # Realizar la asignación de ruta al vehículo
                required_route = {
                    "Origen": request_body["params"]["Origen"],
                    "Destino": request_body["params"]["Destino"]
                }
                routes_loader(vehicle_id, required_route)
            else:
                print("Error: El vehículo con matrícula", matricula, "no está registrado.")
        else:
            print("Error: Faltan parámetros de origen o destino en la solicitud.")
    
    response_json = json.dumps(request_body)
    client.send_rpc_reply(request_id, response_json)


def inicializar_cliente_mqtt():
    """
    Inicializa el cliente MQTT y establece la conexión.
    """
    client = TBDeviceMqttClient(broker, port, token)
    client.connect()
    return client

def obtener_estado_vehiculo():
    vehicle_plate = "ABC123"
    current_steering = 130.5
    current_speed = 150.0
    current_position = (40.7128, -74.0060)  # Latitud y longitud
    current_leds = {"front": "on", "rear": "off"}
    current_ldr = 300
    current_obstacle_distance = 100

    vehicle_status = {
        "vehicle_plate": vehicle_plate,
        "current_steering": current_steering,
        "current_speed": current_speed,
        "current_position": current_position,
        "current_leds": json.dumps(current_leds),
        "current_ldr": current_ldr,
        "current_obstacle_distance": current_obstacle_distance
    }

    return vehicle_status


def publicar_telemetria(client):
    while True:
        vehicle_status = obtener_estado_vehiculo()
        # Agregamos sello de tiempo a los datos de telemetría
        telemetry_with_ts = {"ts": int(round(time.time() * 1000)), "values": vehicle_status}
        print("Datos telemétricos con fecha y hora:", telemetry_with_ts)
        result = client.send_telemetry(telemetry_with_ts)  # Enviar los datos de telemetría con el sello de tiempo
        success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
        print("Resultado de la publicación de telemetría:", success)
        time.sleep(60)


def iniciar_aplicacion():
    # Inicializamos el cliente MQTT al inicio del programa
    client = inicializar_cliente_mqtt()
    client.set_server_side_rpc_request_handler(lambda req_id, body: rpc_request_handler(client, req_id, body))
    telemetry_thread = Thread(target=publicar_telemetria, args=(client,), daemon=True)
    telemetry_thread.start()
    print("Inicio de la publicación de telemetría")

if __name__ == "__main__":
    iniciar_aplicacion()
    print("Starting UVicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8001)

