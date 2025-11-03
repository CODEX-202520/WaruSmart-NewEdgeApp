import os
import socket
import requests


class Esp32Client:
    def __init__(self, actuator_url: str):
        """Inicializa el cliente con la URL del actuador.

        actuator_url: full URL, e.g. http://192.168.1.50/activate or http://esp32-device.local/activate
        """
        self.actuator_url = actuator_url

    def _resolve_host(self):
        """Try to resolve the hostname part of the actuator_url and return IP or None.

        This is a best-effort helper for debugging name resolution issues.
        """
        try:
            # extract hostname from URL
            # naive parsing: remove scheme and path
            url = self.actuator_url
            host_part = url.split('://', 1)[-1].split('/', 1)[0]
            # drop optional port
            host = host_part.split(':', 1)[0]
            ip = socket.gethostbyname(host)
            return host, ip
        except Exception as e:
            return None, str(e)

    def send_activation_request(self, action: str):
        """Envía una solicitud al ESP32 para activar o desactivar un actuador.

        Prints debug info about host resolution to help diagnose NameResolutionError.
        """
        print(f"Esp32Client: invoking actuator_url={self.actuator_url}")

        host, result = self._resolve_host()
        if host:
            print(f"Esp32Client: resolved host '{host}' -> {result}")
        else:
            print(f"Esp32Client: hostname resolution failed: {result}")
            # If environment provides a fallback IP, attempt to use it
            fallback = os.environ.get('ESP32_ACTUATOR_IP')
            if fallback:
                # replace hostname with fallback IP
                try:
                    url = self.actuator_url
                    # replace host portion with fallback (keep scheme and path)
                    scheme = url.split('://', 1)[0]
                    path = url.split('://', 1)[1].split('/', 1)[1] if '/' in url.split('://', 1)[1] else ''
                    new_url = f"{scheme}://{fallback}/{path}" if path else f"{scheme}://{fallback}"
                    print(f"Esp32Client: attempting fallback URL using ESP32_ACTUATOR_IP: {new_url}")
                    response = requests.post(new_url, json={"action": action}, timeout=5)
                    if response.status_code == 200:
                        print(f"Acción {action} activada correctamente (fallback IP).")
                        return
                    else:
                        print(f"Error al activar la acción {action} (fallback). Código: {response.status_code}")
                except requests.RequestException as e:
                    print(f"Error al enviar solicitud al ESP32 usando fallback IP: {e}")

        try:
            # Enviar la solicitud POST al ESP32
            response = requests.post(self.actuator_url, json={"action": action}, timeout=5)

            if response.status_code == 200:
                print(f"Acción {action} activada correctamente.")
            else:
                print(f"Error al activar la acción {action}. Código de respuesta: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error al enviar solicitud al ESP32: {e}")
