import os
from dotenv import dotenv_values  # Cargar variables de entorno
import paho.mqtt.client as mqtt
import time
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
# Cargar variables de entorno
env_vars=dotenv_values('/usr/src/app/.env_vars')

# Acceder a las variables de entorno
api_key=env_vars.get('API_KEY')
api_pass=env_vars.get('API_PASS')
token=env_vars.get('TOKEN')
broker=env_vars.get('BROKER2') 
port=1883


# def on_publish(client, userdata, result): 
#     print("Datos publicados en ThingsBoard \n")
#     pass

# def enviar_datos_thingsboard(broker, port, token):
#     client1 = mqtt.Client("control1")
#     client1.on_publish = on_publish
#     client1.username_pw_set(token)
#     client1.connect(broker, port, keepalive=60)

#     while True:
#         payload = "{" + "\"speed\":90," + "\"time\":90," + "\"strangels\":90" +"}"
#         ret = client1.publish("v1/devices/me/telemetry", payload)
#         print("Por favor revisa tu última telemetría de tu dispositivo")
#         print(payload)
#         time.sleep(5)

def enviar_datos_thingsboard(broker, port, token):
    while True:
        payload = "{" + "\"speed\":180," + "\"time\":180," + "\"strangels\":90" +"}"
        #ret = Client1.publish("v1/devices/me/telemetry", payload)
        print("Por favor revisa tu última telemetría de tu dispositivo")
        print(payload)
        time.sleep(5)

client1 = TBDeviceMqttClient(broker, port, token)
client1.connect()
#enviar_datos_thingsboard(broker, port, token)  # Call the function directly

while True:
    payload = "{"
    payload += "\"SteeringAngle\":100.0,";
    payload += "\"Speed\":90.0,";
    payload += "\"Time\":20.0";
    payload += "}"
    telemetry_with_ts = {"tds": int(round(time.time()*1000)), "values": payload}
    client1.send_telemetry(telemetry_with_ts)  # topic-v1/devices/me/telemetry
    #print("Por favor revisa tu última telemetría de tu dispositivo")
    #print(payload)
    time.sleep(1)


