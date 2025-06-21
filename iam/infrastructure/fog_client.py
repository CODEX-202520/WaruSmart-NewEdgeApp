import requests

class FogClient:
    def __init__(self, fog_url):
        self.fog_url = fog_url
    def register_edge(self, edge_id, device_info):
        try:
            response = requests.post(
                f"{self.fog_url}/api/edge/register",
                json={"edgeId": edge_id, "deviceInfo": device_info}
            )
            if response.status_code == 201 or response.status_code == 200:
                print(f"Edge {edge_id} registrado exitosamente.")
                return response.json()
            else:
                print(f"Error al registrar el Edge: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error en la conexión con el Fog: {e}")