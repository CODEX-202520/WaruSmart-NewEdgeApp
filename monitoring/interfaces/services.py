from flask import Blueprint, request, jsonify
from monitoring.application.services import DeviceMetricApplicationService
from iam.interfaces.services import authenticate_request
import datetime


monitoring_api = Blueprint("monitoring_api", __name__)
device_metric_service = DeviceMetricApplicationService()

@monitoring_api.route("/api/v1/monitoring/device-metrics", methods=["POST"])
def create_device_metrics():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result
    data = request.json
    try:
        device_id = data["device_id"]
        zone = data["zone"]
        soil_moisture = data.get("soil_moisture")
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        created_at = data.get("created_at")
        api_key = request.headers.get("X-API-Key")

        if soil_moisture is None or temperature is None or humidity is None:
            return jsonify({"error": "Faltan valores de métricas"}), 400

        if created_at is None:
            created_at = datetime.datetime.utcnow().isoformat() + "Z"

        metric = device_metric_service.create_device_metric(
            device_id=device_id,
            zone=zone,
            soil_moisture=soil_moisture,
            temperature=temperature,
            humidity=humidity,
            created_at=created_at,
            api_key=api_key
        )

        created_at_value = metric.created_at
        if isinstance(created_at_value, str):
            created_at_str = created_at_value
        else:
            created_at_str = created_at_value.isoformat() + "Z"

        return jsonify({
            "device_id": metric.device_id,
            "zone": metric.zone,
            "soil_moisture": metric.soil_moisture,
            "temperature": metric.temperature,
            "humidity": metric.humidity,
            "created_at": created_at_str
        }), 201

    except KeyError:
        return jsonify({"error": "Faltan campos requeridos"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400