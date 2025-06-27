from flask import Flask, jsonify

from monitoring.infrastructure.models import db, ActuatorModel
from monitoring.infrastructure.repositories import ActuatorRepository
from monitoring.application.services import ActuatorApplicationService
import iam.application.services
from iam.infrastructure.fog_client import FogClient
from iam.interfaces.services import iam_api
from monitoring.interfaces.actuator import actuator_api
from monitoring.interfaces.services import monitoring_api
from shared.infrastructure.database import init_db
import random
import time

app = Flask(__name__)

db.connect()
db.create_tables([ActuatorModel])

# Instancias globales
actuator_repo = ActuatorRepository()
actuator_repo.get_or_create_actuator(device_id="waru-smart-001")
actuator_service = ActuatorApplicationService()

# Registra blueprints
app.register_blueprint(iam_api)
app.register_blueprint(monitoring_api)
app.register_blueprint(actuator_api)

first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        init_db()
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
    timestamp = int(time.time() * 1000)
    sensor_data = {
        'deviceId': 'edge-sector-2',
        'temperature': round(20 + random.random() * 5, 2),
        'humidity': round(60 + random.random() * 10, 2),
        'timestamp': timestamp
    }
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True)


## if __name__ == '__main__':
    ##app.run(debug=True, host='192.168.244.109', port=5000)