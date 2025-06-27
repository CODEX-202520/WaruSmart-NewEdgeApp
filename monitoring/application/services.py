from monitoring.domain.esp32client import Esp32Client
from monitoring.infrastructure.repositories import DeviceMetricRepository, ActuatorRepository
from iam.application.services import AuthApplicationService
from monitoring.domain.entities import DeviceMetric

class DeviceMetricApplicationService:
    def __init__(self):
        self.metric_repository = DeviceMetricRepository()
        self.iam_service = AuthApplicationService()

    def create_device_metric(
        self,
        device_id: str,
        zone: str,
        soil_moisture: float,
        temperature: float,
        humidity: float,
        created_at: str,
        api_key: str
    ) -> DeviceMetric:
        if not self.iam_service.get_by_id_and_api_key(device_id, api_key):
            raise ValueError("ID de dispositivo o API key inválidos")
        metric = DeviceMetric(
            device_id=device_id,
            zone=zone,
            soil_moisture=soil_moisture,
            temperature=temperature,
            humidity=humidity,
            created_at=created_at
        )
        return self.metric_repository.add(metric)


class ActuatorApplicationService:
    def __init__(self):
        from monitoring.infrastructure.repositories import ActuatorRepository
        from monitoring.domain.esp32client import Esp32Client

        self.actuator_repository = ActuatorRepository()
        self.esp32_client = Esp32Client("http://esp32-device.local/activate")

    def activate_actuator(self, device_id, action, created_at, api_key):
        actuator = self.actuator_repository.get_actuator_by_device_id(device_id)

        if not actuator:
            raise ValueError(f"No actuator found for device_id: {device_id}")

        if action == "irrigate":
            actuator.activate()
            self.actuator_repository.save(actuator)
            self.esp32_client.send_activation_request(action)
            return actuator
        elif action == "deactivate":
            actuator.deactivate()
            self.actuator_repository.save(actuator)
            self.esp32_client.send_activation_request(action)
            return actuator
        else:
            raise ValueError("Unknown action")
