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
        timestamp: datetime,
        metric_type: MetricType,
        value: float,
        zone_id: Optional[str] = None,
        unit: Optional[str] = None
    ):
        self.device_id = device_id
        self.timestamp = timestamp
        self.metric_type = metric_type
        self.value = value
        self.zone_id = zone_id
        self.unit = unit