from datetime import datetime
from typing import Optional

import peewee

from iam.domain.entities import Device
from iam.infrastructure.models import Device as DeviceModel


class DeviceRepository:
    @staticmethod
    def find_by_id_and_api_key(device_id:str, api_key:str) -> Optional[Device]:
        """find a device by itsID and api_key
        """
        try:
            device =DeviceModel.get(
                (DeviceModel.device_id == device_id) &
                (DeviceModel.api_key == api_key)
            )
            return Device(device.device_id, device.api_key, device.created_at)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def get_or_create_test_device()->Device:
        device, _ = DeviceModel.get_or_create(
            device_id='waru-smart-001',
            defaults={"api_key": "test-api-key-123", "created_at": datetime.now().isoformat()}
        )
        return Device(device.device_id, device.api_key, device.created_at)

