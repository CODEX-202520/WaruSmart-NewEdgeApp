from flask import Blueprint, request, jsonify
from monitoring.application.services import DeviceMetricApplicationService
from monitoring.infrastructure.models import DeviceConfigModel
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

@monitoring_api.route("/api/v1/device-config", methods=["POST"])
def update_device_config():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result
        
    data = request.json
    required_fields = [
        "soil_moisture_min_device",
        "temperature_max_device",
        "humidity_min_device",
        "overwrite_automation",
        "manually_active",
        "device_id",
        "parcela_id"
    ]
    
    # Verificar que todos los campos requeridos estén presentes
    if not all(field in data for field in required_fields):
        return jsonify({
            "error": "Faltan campos requeridos",
            "required_fields": required_fields
        }), 400
    
    try:
        # Convertir valores a los tipos correctos
        device_id = str(data["device_id"])
        parcela_id = str(data["parcela_id"])
        soil_moisture_min = float(data["soil_moisture_min_device"])
        temperature_max = float(data["temperature_max_device"])
        humidity_min = float(data["humidity_min_device"])
        overwrite_automation = bool(data["overwrite_automation"])
        manually_active = bool(data["manually_active"])
        
        # Validar rangos
        if not (0 <= soil_moisture_min <= 100):
            return jsonify({"error": "soil_moisture_min_device debe estar entre 0 y 100"}), 400
        if not (0 <= humidity_min <= 100):
            return jsonify({"error": "humidity_min_device debe estar entre 0 y 100"}), 400
        if not (-20 <= temperature_max <= 60):
            return jsonify({"error": "temperature_max_device debe estar entre -20 y 60"}), 400
        
        # Actualizar o crear configuración
        config, created = DeviceConfigModel.get_or_create(
            device_id=device_id,
            defaults={
                "parcela_id": parcela_id,
                "soil_moisture_min_device": soil_moisture_min,
                "temperature_max_device": temperature_max,
                "humidity_min_device": humidity_min,
                "overwrite_automation": overwrite_automation,
                "manually_active": manually_active
            }
        )
        
        if not created:
            config.parcela_id = parcela_id
            config.soil_moisture_min_device = soil_moisture_min
            config.temperature_max_device = temperature_max
            config.humidity_min_device = humidity_min
            config.overwrite_automation = overwrite_automation
            config.manually_active = manually_active
            config.updated_at = datetime.datetime.now()
            config.save()

        return jsonify({
            "message": "Configuración actualizada correctamente",
            "device_id": device_id,
            "parcela_id": parcela_id,
            "soil_moisture_min_device": soil_moisture_min,
            "temperature_max_device": temperature_max,
            "humidity_min_device": humidity_min,
            "overwrite_automation": overwrite_automation,
            "manually_active": manually_active,
            "updated_at": config.updated_at.isoformat() + "Z"
        }), 200

    except ValueError as e:
        return jsonify({"error": f"Error en el formato de los datos: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500