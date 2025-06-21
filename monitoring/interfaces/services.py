from flask import Blueprint, request, jsonify
from monitoring.application.services import DeviceMetricApplicationService
from iam.interfaces.services import authenticate_request
import datetime

monitoring_api = Blueprint("monitoring_api", __name__)
device_metric_service = DeviceMetricApplicationService()

@monitoring_api.route("/api/v1/monitoring/device-metrics", methods=["POST"])
def create_device_metric():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result
    data = request.json
    try:
        device_id = data["device_id"]
        metric_type = data["metric_type"]
        value = data["value"]
        zone = data["zone"]
        unit = data["unit"]
        created_at = datetime.datetime.now()
        metric = device_metric_service.create_device_metric(
            device_id, metric_type, value, zone, unit, created_at, request.headers.get("X-API-Key")
        )
        return jsonify({
            "device_id": metric.device_id,
            "metric_type": str(metric.metric_type.value),  # <-- Convierte a string
            "value": metric.value,
            "zone": metric.zone,
            "unit": metric.unit,
            "created_at": metric.created_at,
            "status": metric.status
        }), 201
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400