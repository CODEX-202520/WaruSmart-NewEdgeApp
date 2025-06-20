from typing import List, Optional
from monitoring.domain.entities import DeviceMetric, Actuator
from monitoring.infrastructure.models import DeviceMetricModel
import peewee

class DeviceMetricRepository:
    @staticmethod
    def find_by_device_id(device_id: str) -> List[DeviceMetric]:
        metrics = DeviceMetricModel.select().where(DeviceMetricModel.device_id == device_id)
        return [
            DeviceMetric(
                device_id=m.device_id,
                created_at=m.timestamp,
                metric_type=m.metric_type,
                value=m.value,
                zone=m.zone,
                unit=m.unit
            )
            for m in metrics
        ]

    @staticmethod
    def add(metric: DeviceMetric) -> DeviceMetric:
        DeviceMetricModel.create(
            device_id=metric.device_id,
            timestamp=metric.created_at,
            metric_type=metric.metric_type,
            value=metric.value,
            zone=metric.zone,
            unit=metric.unit
        )
        return metric

class ActuatorRepository:
    def __init__(self):
        # Simulamos una base de datos en memoria
        self.actuators_db = {}

    def get_actuator_by_device_id(self, device_id: str) -> Optional[Actuator]:
        """Obtiene un actuador por su ID de dispositivo."""
        return self.actuators_db.get(device_id)

    def save(self, actuator: Actuator):
        """Guarda o actualiza el actuador en la base de datos."""
        self.actuators_db[actuator.device_id] = actuator

    def get_all_actuators(self):
        """Obtiene todos los actuadores almacenados."""
        return list(self.actuators_db.values())

    def delete(self, device_id: str):
        """Elimina un actuador de la base de datos."""
        if device_id in self.actuators_db:
            del self.actuators_db[device_id]