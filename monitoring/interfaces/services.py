from abc import ABC, abstractmethod
from typing import List
from monitoring.domain.entities import DeviceMetric

class IDeviceMetricService(ABC):
    @abstractmethod
    def get_metrics_by_device_id(self, device_id: str) -> List[DeviceMetric]:
        pass

    @abstractmethod
    def add_metric(self, metric: DeviceMetric) -> DeviceMetric:
        pass

    @abstractmethod
    def update_metric(self, metric: DeviceMetric) -> DeviceMetric:
        pass

    @abstractmethod
    def delete_metric(self, metric_id: str) -> None:
        pass