
from flask import Flask, jsonify, request

from monitoring.infrastructure.models import db, ActuatorModel
from monitoring.infrastructure.repositories import ActuatorRepository
from monitoring.application.services import ActuatorApplicationService, DeviceMetricApplicationService
import iam.application.services
from iam.interfaces.services import iam_api
from monitoring.interfaces.actuator import actuator_api
from monitoring.interfaces.services import monitoring_api
from shared.infrastructure.database import init_db

app = Flask(__name__)

db.connect()
db.create_tables([ActuatorModel])

# Instancias globales
actuator_repo = ActuatorRepository()
actuator_repo.get_or_create_actuator(device_id="waru-smart-001")
actuator_service = ActuatorApplicationService()
device_metric_service = DeviceMetricApplicationService()

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

@app.route('/sensor', methods=['GET'])
def get_sensor_data():
    device_id = request.args.get('device_id', 'waru-smart-001')
    
    # Obtener última métrica
    last_metric = device_metric_service.get_last_metric_by_device(device_id)
    if not last_metric:
        return jsonify({"mensaje": "No hay datos disponibles"}), 200

    # Formatear timestamp
    created_at_value = last_metric.created_at
    if isinstance(created_at_value, str):
        created_at_str = created_at_value
    else:
        created_at_str = created_at_value.isoformat() + "Z"

    # Obtener estado del actuador
    actuator = actuator_repo.get_actuator_by_device_id(device_id)
    
    # Obtener configuración del dispositivo
    try:
        from monitoring.infrastructure.models import DeviceConfigModel
        config = DeviceConfigModel.get(DeviceConfigModel.device_id == device_id)
        device_config = {
            "parcela_id": config.parcela_id,
            "soil_moisture_min_device": config.soil_moisture_min_device,
            "temperature_max_device": config.temperature_max_device,
            "humidity_min_device": config.humidity_min_device,
            "overwrite_automation": config.overwrite_automation,
            "manually_active": config.manually_active
        }
    except DeviceConfigModel.DoesNotExist:
        device_config = {
            "parcela_id": None,
            "soil_moisture_min_device": 50.0,  # valor por defecto
            "temperature_max_device": 30.0,    # valor por defecto
            "humidity_min_device": 35.0,       # valor por defecto
            "overwrite_automation": False,
            "manually_active": False
        }

    result = {
        "device": {
            "deviceId": last_metric.device_id,
            "zone": last_metric.zone,
            "parcela_id": device_config["parcela_id"]
        },
        "current_metrics": {
            "soil_moisture": last_metric.soil_moisture,
            "temperature": last_metric.temperature,
            "humidity": last_metric.humidity,
            "timestamp": created_at_str
        },
        "device_config": {
            "thresholds": {
                "soil_moisture_min": device_config["soil_moisture_min_device"],
                "temperature_max": device_config["temperature_max_device"],
                "humidity_min": device_config["humidity_min_device"]
            },
            "automation": {
                "overwrite_automation": device_config["overwrite_automation"],
                "manually_active": device_config["manually_active"]
            }
        },
        "actuator_status": {
            "status": "active" if actuator and actuator.status else "inactive",
            "type": actuator.actuator_type if actuator else "unknown"
        }
    }
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)



## if __name__ == '__main__':
    ##app.run(debug=True, host='192.168.244.109', port=5000)