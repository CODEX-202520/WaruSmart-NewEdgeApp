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
        self.status = self._calculate_status()

    def _calculate_status(self) -> str:
        if self.metric_type == MetricType.TEMPERATURE:
            if self.value < 18:
                return "Temperatura baja"
            elif 18 <= self.value <= 28:
                return "Temperatura Normal "
            else:
                return "Temperatura alta"
        elif self.metric_type == MetricType.SOIL_MOISTURE:
            if self.value < 35:
                return "Humedad del suelo baja"
            elif 35 <= self.value <= 65:
                return "Humedad del suelo Normal"
            else:
                return "Humedad del suelo alta"
        elif self.metric_type == MetricType.HUMIDITY:
            if self.value < 40:
                return "Humedad ambiental baja"
            elif 40 <= self.value <= 70:
                return "Humedad ambiental Normal"
            else:
                return "Humedad ambiental alta"
        else:
            return "Tipo de métrica desconocido"

class Actuator:
    def __init__(self, device_id: str, actuator_type: str, status: bool = False):
        self.device_id = device_id
        self.actuator_type = actuator_type
        self.status = status

    def activate(self):
        self.status = True

    def deactivate(self):
        self.status = False