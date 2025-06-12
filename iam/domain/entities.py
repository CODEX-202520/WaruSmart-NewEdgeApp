"""
Domain entities for the IAM module
"""
class Device:
    """
    Represents a device in the IAM System
    """
    def __init__(self, device_id:str, api_key:str, created_at:str):
        self.device_id = device_id
        self.api_key = api_key
        self.created_at = created_at

