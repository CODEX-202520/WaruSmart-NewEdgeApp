from flask import Blueprint, request, jsonify
from monitoring.infrastructure.repositories import DeviceMetricRepository
from monitoring.application.services import ActuatorApplicationService

actuator_api = Blueprint('actuator_api', __name__)

@actuator_api.route('/api/v1/actuators/status', methods=['POST'])
def auto_actuate():
    device_id = request.json.get("device_id")
    if not device_id:
        return jsonify({"error": "device_id requerido"}), 400

    metric_repo = DeviceMetricRepository()
    last_metric = metric_repo.get_last_metric_by_device_id(device_id)
    if not last_metric:
        return jsonify({"error": "No hay métricas para este dispositivo"}), 404

    soil_moisture = last_metric.soil_moisture
    temperature = last_metric.temperature
    humidity = last_metric.humidity

    # Lógica de decisión
    if soil_moisture < 30 or (temperature > 30 and humidity < 40):
        action = "irrigate"
    else:
        action = "deactivate"

    actuator_service = ActuatorApplicationService()
    actuator_service.activate_actuator(device_id, action, last_metric.created_at, "api_key")  # Ajusta api_key según tu lógica

    return jsonify({
        "status": "success",
        "action": action,
        "soil_moisture": soil_moisture,
        "temperature": temperature,
        "humidity": humidity
    })