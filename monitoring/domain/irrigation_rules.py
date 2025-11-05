from monitoring.infrastructure.models import DeviceConfigModel

class IrrigationRules:
    @staticmethod
    def should_irrigate(device_id: str, soil_moisture: float, temperature: float, humidity: float) -> bool:
        """
        Irrigation rules based on device-specific configuration thresholds
        Args:
            device_id: The ID of the device to get configuration for
            soil_moisture: Current soil moisture reading
            temperature: Current temperature reading
            humidity: Current humidity reading
        Returns:
            bool: True if irrigation should be activated
        """
        try:
            # Obtener la configuración específica del dispositivo
            config = DeviceConfigModel.get(DeviceConfigModel.device_id == device_id)
            
            # Si la automatización está sobreescrita, usar el valor manual
            if config.overwrite_automation:
                return config.manually_active
            
            # Si no, usar los umbrales configurados para el dispositivo
            moisture_condition = soil_moisture < config.soil_moisture_min_device
            temp_humidity_condition = (temperature > config.temperature_max_device and 
                                    humidity < config.humidity_min_device)
            
            return moisture_condition or temp_humidity_condition
            
        except DeviceConfigModel.DoesNotExist:
            # Si no hay configuración, usar valores por defecto
            DEFAULT_SOIL_MOISTURE_MIN = 50
            DEFAULT_TEMPERATURE_MAX = 30
            DEFAULT_HUMIDITY_MIN = 35
            
            print(f"WARNING: No configuration found for device {device_id}, using default values")
            return soil_moisture < DEFAULT_SOIL_MOISTURE_MIN or (
                temperature > DEFAULT_TEMPERATURE_MAX and humidity < DEFAULT_HUMIDITY_MIN
            )