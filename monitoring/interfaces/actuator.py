from flask import Blueprint, request, jsonify
from monitoring.infrastructure.repositories import DeviceMetricRepository
from monitoring.application.services import ActuatorApplicationService
from monitoring.domain.irrigation_rules import IrrigationRules
from monitoring.infrastructure.fog_client import FogClient

actuator_api = Blueprint('actuator_api', __name__)
fog_client = FogClient()  # Crea una instancia única del FogClient

@actuator_api.route('/api/v1/actuators/status', methods=['POST'])
def auto_actuate():
    device_id = request.json.get("device_id")
    if not device_id:
        return jsonify({"error": "device_id requerido"}), 400

    metric_repo = DeviceMetricRepository()
    last_metric = metric_repo.get_last_metric_by_device_id(device_id)
    if not last_metric:
        return jsonify({"error": "No hay métricas para este dispositivo"}), 404

    # Obtener la fase fenológica actual del cultivo usando el FogClient con caché
    phenological_phase = fog_client.get_phenological_phase(device_id)

    soil_moisture = last_metric.soil_moisture
    temperature = last_metric.temperature
    humidity = last_metric.humidity

    # Obtener la fase fenológica y sus umbrales correspondientes
    phase = fog_client.get_phenological_phase(device_id)
    thresholds = fog_client.get_irrigation_thresholds(phase)
    
    print("\n=== Estado Actual del Cultivo ===")
    print(f"Fase Fenológica: {phase}")
    print(f"Condiciones actuales:")
    print(f"- Humedad del suelo: {soil_moisture}%")
    print(f"- Temperatura: {temperature}°C")
    print(f"- Humedad ambiental: {humidity}%")
    print("\nUmbrales para esta fase:")
    print(f"- Humedad del suelo mínima: {thresholds['soil_moisture_min']}%")
    print(f"- Temperatura máxima: {thresholds['temperature_max']}°C")
    print(f"- Humedad ambiental mínima: {thresholds['humidity_min']}%")

    # Evaluar cada condición por separado
    moisture_condition = soil_moisture < thresholds["soil_moisture_min"]
    temp_humidity_condition = (temperature > thresholds["temperature_max"] and 
                             humidity < thresholds["humidity_min"])
    
    should_irrigate = moisture_condition or temp_humidity_condition
    
    print("\nEvaluación de condiciones:")
    print(f"1. ¿Humedad del suelo muy baja? {'SÍ' if moisture_condition else 'NO'}")
    print(f"2. ¿Temperatura alta y humedad baja? {'SÍ' if temp_humidity_condition else 'NO'}")
    
    # Si estamos en fase de Ripening o HarvestReady, nunca regar
    if phase in ["Ripening", "HarvestReady"]:
        should_irrigate = False
        print("\nFase de maduración o cosecha detectada - Se deshabilita el riego")

    action = "irrigate" if should_irrigate else "deactivate"
    print(f"\nDecisión final: {'ACTIVAR' if should_irrigate else 'DESACTIVAR'} el riego")
    print("================================\n")

    actuator_service = ActuatorApplicationService()
    actuator_service.activate_actuator(
        device_id, 
        action, 
        last_metric.created_at, 
        "api_key",  # Ajusta api_key según tu lógica
        phenological_phase
    )

    return jsonify({
        "status": "success",
        "action": action,
        "soil_moisture": soil_moisture,
        "temperature": temperature,
        "humidity": humidity
    })