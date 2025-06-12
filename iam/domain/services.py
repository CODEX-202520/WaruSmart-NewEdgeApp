from typing import Optional

from iam.domain.entities import Device


class AuthService:
    def __init__(self):
        pass

    @staticmethod
    def authenticate(device: Optional[Device]) -> bool:
        """Authenticates a device.
        Args:
            device (Optional[Device]): The device to authenticate.

        Returns:
            bool: True if the authentication was successful, False otherwise.
        """
        return device is not None
