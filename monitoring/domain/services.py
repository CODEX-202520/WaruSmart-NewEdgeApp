from datetime import timezone, datetime
from dateutil.parser import parse
from monitoring.domain.entities import DeviceMetric

class MonitoringDomainService:
    """Servicio para gestionar métricas de dispositivos."""
    def __init__(self):
        pass

    @staticmethod
    def create_metric(
            device_id: str,
            zone: str,
            soil_moisture: float,
            temperature: float,
            humidity: float,
            created_at: str | None = None
    ) -> DeviceMetric:
        """
        Crea una instancia de DeviceMetric con los tres valores.
        """
        try:
            soil_moisture = float(soil_moisture)
            temperature = float(temperature)
            humidity = float(humidity)
            if soil_moisture < 0 or humidity < 0:
                raise ValueError("La humedad del suelo y la humedad ambiental no pueden ser negativas.")
            if created_at:
                parsed_created_at = parse(created_at).astimezone(timezone.utc)
            else:
                parsed_created_at = datetime.now(timezone.utc)
        except (ValueError, TypeError):
            raise ValueError("Entrada inválida para los valores o created_at.")
        return DeviceMetric(
            device_id=device_id,
            created_at=parsed_created_at,
            zone=zone,
            soil_moisture=soil_moisture,
            temperature=temperature,
            humidity=humidity
        )