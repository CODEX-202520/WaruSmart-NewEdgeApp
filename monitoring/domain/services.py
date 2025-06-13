from datetime import timezone, datetime
from dateutil.parser import parse
from monitoring.domain.entities import DeviceMetric

class MonitoringDomainService:
    """Service for managing device metrics."""
    def __init__(self):
        pass

    @staticmethod
    def create_metric(
        device_id: str,
        metric_type: str,
        value: float,
        zone: str,
        unit: str,
        created_at: str | None = None
    ) -> DeviceMetric:
        """
        Creates a DeviceMetric instance.
        Args:
            device_id (str): Identifier for the device.
            metric_type (str): Type of metric (e.g., temperature, humidity).
            value (float): Value of the metric.
            zone (str): Zone or location of the device.
            unit (str): Unit of the metric.
            created_at (str | None): Timestamp in ISO format.
        Returns:
            DeviceMetric: An instance of DeviceMetric with validated data.
        """
        try:
            value = float(value)
            if value < 0:
                raise ValueError("Metric value cannot be negative.")
            if created_at:
                parsed_created_at = parse(created_at).astimezone(timezone.utc)
            else:
                parsed_created_at = datetime.now(timezone.utc)
        except (ValueError, TypeError):
            raise ValueError("Invalid input for value or created_at.")
        return DeviceMetric(
            device_id=device_id,
            metric_type=metric_type,
            value=value,
            zone=zone,
            unit=unit,
            created_at=parsed_created_at
        )