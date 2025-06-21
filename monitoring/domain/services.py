from datetime import timezone, datetime
from dateutil.parser import parse
from monitoring.domain.entities import DeviceMetric, MetricType

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
        """
        try:
            value = float(value)
            if value < 0:
                raise ValueError("Metric value cannot be negative.")
        except (ValueError, TypeError):
            raise ValueError("Invalid input for value.")

        if created_at:
            try:
                parsed_created_at = parse(created_at).astimezone(timezone.utc)
            except Exception:
                raise ValueError("Invalid input for created_at.")
        else:
            parsed_created_at = datetime.now(timezone.utc)

        try:
            metric_type_enum = MetricType(metric_type)
        except ValueError:
            raise ValueError("Tipo de métrica inválido.")

        return DeviceMetric(
            device_id=device_id,
            metric_type=metric_type_enum,
            value=value,
            zone=zone,
            unit=unit,
            created_at=parsed_created_at
        )