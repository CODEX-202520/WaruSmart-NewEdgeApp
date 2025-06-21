from flask import Flask, jsonify

import iam.application.services
from iam.infrastructure.fog_client import FogClient
from iam.interfaces.services import iam_api
from monitoring.interfaces.actuator import actuator_api
from monitoring.interfaces.services import monitoring_api  # importa tu blueprint de métricas
from shared.infrastructure.database import init_db
import random
import time
from datetime import datetime
import pytz

app = Flask(__name__)

app.register_blueprint(iam_api)
app.register_blueprint(monitoring_api)  # registra el blueprint de métricas
app.register_blueprint(actuator_api)

first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        init_db() # Inicializacion de la base de datos

        auth_application_service = iam.application.services.AuthApplicationService()
        auth_application_service.get_or_create_test_device()

        fog_client = FogClient(fog_url='http://localhost:8080')
        edge_id = 'edge-sector-2'
        device_info = 'Edge 2 de la hectarea 2'
        response = fog_client.register_edge(edge_id, device_info)
        if response:
            print(f"Edge {edge_id} registrado exitosamente.")
        else:
            print(f"Error al registrar el Edge {edge_id}.")

@app.route('/sensor', methods=['GET'])
def get_sensor_data():
    timestamp = int(time.time() * 1000)  # Timestamp en milisegundos desde Epoch

    sensor_data = {
        'deviceId': 'edge-sector-2',  # ID del Edge
        'temperature': round(20 + random.random() * 5, 2),  # Temperatura entre 20 y 25
        'humidity': round(60 + random.random() * 10, 2),  # Humedad entre 60 y 70
        'timestamp': timestamp  # Timestamp en milisegundos
    }
    return jsonify(sensor_data)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.244.109', port=5000)