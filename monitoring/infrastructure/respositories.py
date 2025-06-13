from typing import List
from monitoring.domain.entities import DeviceMetric
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