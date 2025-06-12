
from typing import List
from monitoring.domain.entities import DeviceMetric
from monitoring.infrastructure.respositories import DeviceMetricRepository


class DeviceMetricService:
    @staticmethod
    def get_metrics_by_device_id(device_id: str) -> List[DeviceMetric]:
        return DeviceMetricRepository.find_by_device_id(device_id)

    @staticmethod
    def add_metric(metric: DeviceMetric) -> DeviceMetric:
        return DeviceMetricRepository.add(metric)