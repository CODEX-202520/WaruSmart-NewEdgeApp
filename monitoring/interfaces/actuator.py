from flask import Blueprint, request, jsonify
from monitoring.infrastructure.repositories import DeviceMetricRepository
from monitoring.application.services import ActuatorApplicationService
from monitoring.domain.irrigation_rules import IrrigationRules
from monitoring.infrastructure.models import DeviceConfigModel

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

    # Evaluar si debe regar usando las reglas de irrigación configuradas
    irrigation_rules = IrrigationRules()
    should_irrigate = irrigation_rules.should_irrigate(
        device_id=device_id,
        soil_moisture=soil_moisture,
        temperature=temperature,
        humidity=humidity
    )

    print("\n=== Estado Actual del Cultivo ===")
    print(f"\nCondiciones actuales:")
    print(f"- Humedad del suelo: {soil_moisture}%")
    print(f"- Temperatura: {temperature}°C")
    print(f"- Humedad ambiental: {humidity}%")
    
    try:
        config = DeviceConfigModel.get(DeviceConfigModel.device_id == device_id)
        print("\nConfiguración del dispositivo:")
        print(f"- Humedad mínima configurada: {config.soil_moisture_min_device}%")
        print(f"- Temperatura máxima configurada: {config.temperature_max_device}°C")
        print(f"- Humedad mínima configurada: {config.humidity_min_device}%")
        print(f"- Control manual: {'ACTIVADO' if config.overwrite_automation else 'DESACTIVADO'}")
        if config.overwrite_automation:
            print(f"- Estado manual: {'ENCENDIDO' if config.manually_active else 'APAGADO'}")
    except DeviceConfigModel.DoesNotExist:
        print("\nUsando valores por defecto (no hay configuración específica)")
        print("- Humedad mínima: 50%")
        print("- Temperatura máxima: 30°C")
        print("- Humedad mínima: 35%")
    
    action = "irrigate" if should_irrigate else "deactivate"
    print(f"\nDecisión final: {'ACTIVAR' if should_irrigate else 'DESACTIVAR'} el riego")
    print("================================\n")

    actuator_service = ActuatorApplicationService()
    actuator_service.activate_actuator(
        device_id, 
        action, 
        last_metric.created_at, 
        "api_key"
    )

    return jsonify({
        "status": "success",
        "action": action,
        "soil_moisture": soil_moisture,
        "temperature": temperature,
        "humidity": humidity
    })