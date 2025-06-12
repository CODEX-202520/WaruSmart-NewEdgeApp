# monitoring/domain/services.py
from typing import List
from .entities import DeviceMetric

class MonitoringDomainService:
    def add_metrics(self, metrics: List[DeviceMetric]) -> List[DeviceMetric]:
        for metric in metrics:
            self.validate_metric(metric)
        return metrics

    def validate_metric(self, metric: DeviceMetric):
        if metric.value < 0:
            raise ValueError("Metric value cannot be negative")