FROM python:3.11.1

#ADD VehicleDigitalTwin.py /

#ENV PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copiamos el código fuente desde la carpeta local "./code" al directorio de trabajo del contenedor "/usr/src/app"
COPY ./code /usr/src/app/code

# Copiamos el archivo de variables de entorno
COPY .env_vars /usr/src/app/.env_vars

ADD requirements.txt /
# Instalamos las dependencias necesarias
RUN pip install -r  /requirements.txt

# Comando por defecto para ejecutar la aplicación
CMD ["python", "/usr/src/app/code/VehicleDigitalTwin.py"]












