from enum import Enum
from typing import Optional
from datetime import datetime

class MetricType(Enum):
    SOIL_MOISTURE = "soil_moisture"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"

class DeviceMetric:
    def __init__(
        self,
        device_id: str,
        created_at: datetime,
        metric_type: MetricType,
        value: float,
        zone: Optional[str] = None,
        unit: Optional[str] = None
    ):
        self.device_id = device_id
        self.created_at = created_at
        self.metric_type = metric_type
        self.value = value
        self.zone = zone
        self.unit = unit


class Actuator:
    def __init__(self, device_id: str, actuator_type: str, status: bool = False):
        self.device_id = device_id
        self.actuator_type = actuator_type
        self.status = status

    def activate(self):
        self.status = True

    def deactivate(self):
        self.status = False
