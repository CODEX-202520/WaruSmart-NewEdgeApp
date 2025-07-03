
from flask import Flask, jsonify, request

from monitoring.infrastructure.models import db, ActuatorModel
from monitoring.infrastructure.repositories import ActuatorRepository
from monitoring.application.services import ActuatorApplicationService, DeviceMetricApplicationService
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
device_metric_service = DeviceMetricApplicationService()

fog_client = None  # Declara globalmente

sensor_index = 0

# Registra blueprints
app.register_blueprint(iam_api)
app.register_blueprint(monitoring_api)
app.register_blueprint(actuator_api)

first_request = True

@app.before_request
def setup():
    global first_request, fog_client
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
    global sensor_index
    device_id = request.args.get('device_id', 'waru-smart-001')
    metrics = device_metric_service.get_all_metrics_by_device(device_id)
    if not metrics:
        return jsonify({"mensaje": "No hay datos disponibles"}), 200

    if sensor_index >= len(metrics):
        return jsonify({"mensaje": "No hay más datos"}), 200

    metric = metrics[sensor_index]
    sensor_index += 1

    created_at_value = metric.created_at
    if isinstance(created_at_value, str):
        created_at_str = created_at_value
    else:
        created_at_str = created_at_value.isoformat() + "Z"

    result = {
        "deviceId": metric.device_id,
        "zone": metric.zone,
        "soil_moisture": metric.soil_moisture,
        "temperature": metric.temperature,
        "humidity": metric.humidity,
        "timestamp": created_at_str
    }
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)



## if __name__ == '__main__':
    ##app.run(debug=True, host='192.168.244.109', port=5000)