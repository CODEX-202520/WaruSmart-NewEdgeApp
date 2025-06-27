from enum import Enum
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
        zone: str,
        soil_moisture: float,
        temperature: float,
        humidity: float
    ):
        self.device_id = device_id
        self.created_at = created_at
        self.zone = zone
        self.soil_moisture = soil_moisture
        self.temperature = temperature
        self.humidity = humidity


class Actuator:
    def __init__(self, device_id: str, actuator_type: str, status: bool = False):
        self.device_id = device_id
        self.actuator_type = actuator_type
        self.status = status

    def activate(self):
        self.status = True

    def deactivate(self):
        self.status = False