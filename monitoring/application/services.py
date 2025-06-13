from monitoring.domain.entities import DeviceMetric
from monitoring.infrastructure.respositories import DeviceMetricRepository
from iam.application.services import AuthApplicationService

class DeviceMetricApplicationService:
    def __init__(self):
        self.metric_repository = DeviceMetricRepository()
        self.iam_service = AuthApplicationService()

    def create_device_metric(self, device_id: str, metric_type: str, value: float, zone: str, unit: str,
                             created_at: str, api_key: str) -> DeviceMetric:
        if not self.iam_service.get_by_id_and_api_key(device_id, api_key):
            raise ValueError("ID de dispositivo o API key inválidos")
        metric = DeviceMetric(
            device_id=device_id,
            metric_type=metric_type,
            value=value,
            zone=zone,
            unit=unit,
            created_at=created_at
        )
        return self.metric_repository.add(metric)