from typing import List, Optional
from monitoring.domain.entities import DeviceMetric, Actuator
from monitoring.infrastructure.models import DeviceMetricModel, ActuatorModel
from datetime import datetime
import peewee

class DeviceMetricRepository:
    @staticmethod
    def find_by_device_id(device_id: str) -> List[DeviceMetric]:
        metrics = DeviceMetricModel.select().where(DeviceMetricModel.device_id == device_id)
        return [
            DeviceMetric(
                device_id=m.device_id,
                created_at=m.created_at,
                zone=m.zone,
                soil_moisture=m.soil_moisture,
                temperature=m.temperature,
                humidity=m.humidity
            )
            for m in metrics
        ]

    @staticmethod
    def add(metric: DeviceMetric) -> DeviceMetric:
        created_at = metric.created_at = datetime.now().isoformat()
        DeviceMetricModel.create(
            device_id=metric.device_id,
            created_at=created_at,
            zone=metric.zone,
            soil_moisture=metric.soil_moisture,
            temperature=metric.temperature,
            humidity=metric.humidity
        )
        return metric

    @staticmethod
    def get_last_metric_by_device_id(device_id: str) -> Optional[DeviceMetric]:
        m = (
            DeviceMetricModel
            .select()
            .where(DeviceMetricModel.device_id == device_id)
            .order_by(DeviceMetricModel.created_at.desc())
            .first()
        )
        if not m:
            return None
        return DeviceMetric(
            device_id=m.device_id,
            created_at=m.created_at,
            zone=m.zone,
            soil_moisture=m.soil_moisture,
            temperature=m.temperature,
            humidity=m.humidity
        )

class ActuatorRepository:
    @staticmethod
    def get_actuator_by_device_id(device_id: str) -> Optional[Actuator]:
        try:
            actuator = ActuatorModel.get(ActuatorModel.device_id == device_id)
            return Actuator(
                device_id=actuator.device_id,
                status=actuator.status,
                actuator_type=actuator.actuator_type
            )
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def save(actuator: Actuator):
        ActuatorModel.insert(
            device_id=actuator.device_id,
            status=actuator.status,
            actuator_type=actuator.actuator_type,
            created_at=datetime.now().isoformat()
        ).on_conflict_replace().execute()

    @staticmethod
    def get_all_actuators() -> List[Actuator]:
        actuators = ActuatorModel.select()
        return [
            Actuator(
                device_id=a.device_id,
                status=a.status,
                actuator_type=a.actuator_type
            )
            for a in actuators
        ]

    @staticmethod
    def get_or_create_actuator(device_id: str, status: str = "inactive", actuator_type: str = "relay") -> Actuator:
        actuator, created = ActuatorModel.get_or_create(
            device_id=device_id,
            defaults={
                "status": status,
                "actuator_type": actuator_type,
                "created_at": datetime.now().isoformat()
            }
        )
        return Actuator(
            device_id=actuator.device_id,
            status=actuator.status,
            actuator_type=actuator.actuator_type
        )