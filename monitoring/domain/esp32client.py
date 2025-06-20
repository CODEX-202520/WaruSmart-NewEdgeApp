import requests

class Esp32Client:
    def __init__(self, actuator_url: str):
        """Inicializa el cliente con la URL del actuador."""
        self.actuator_url = actuator_url

    def send_activation_request(self, action: str):
        """Envía una solicitud al ESP32 para activar o desactivar un actuador."""
        try:
            # Enviar la solicitud POST al ESP32
            response = requests.post(self.actuator_url, json={"action": action})

            if response.status_code == 200:
                print(f"Acción {action} activada correctamente.")
            else:
                print(f"Error al activar la acción {action}. Código de respuesta: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error al enviar solicitud al ESP32: {e}")
