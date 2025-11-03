import requests
import time
from datetime import datetime, timedelta

import sqlite3
from datetime import datetime, timedelta
import json

class FogClient:
    def __init__(self, base_url="http://localhost:8080", db_path="edge_cache.db"):
        self.base_url = base_url
        self.db_path = db_path
        self.setup_database()
        print(f"FogClient initialized with base_url: {self.base_url}")

    def setup_database(self):
        """Configura la base de datos local para el caché"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Tabla para almacenar las fases fenológicas por dispositivo
        c.execute('''CREATE TABLE IF NOT EXISTS device_phases
                    (device_id TEXT PRIMARY KEY,
                     phenological_phase TEXT,
                     last_updated TIMESTAMP,
                     manually_active BOOLEAN,
                     overwrite_automation BOOLEAN)''')
        
        # Tabla para almacenar los umbrales de riego por fase
        c.execute('''CREATE TABLE IF NOT EXISTS irrigation_thresholds
                    (phase TEXT PRIMARY KEY,
                     soil_moisture_min FLOAT,
                     temperature_max FLOAT,
                     humidity_min FLOAT)''')
        
        # Insertar o actualizar los umbrales por defecto
        thresholds = {
            "Germination": (60, 30, 40),
            "Tillering": (50, 28, 35),
            "StemElongation": (45, 30, 30),
            "Booting": (50, 32, 35),
            "Heading": (55, 30, 40),
            "Flowering": (60, 32, 35),
            "GrainFilling": (50, 33, 30),
            "Ripening": (35, 100, 0),  # Valores altos para evitar riego
            "HarvestReady": (0, 100, 0)  # Nunca regar
        }
        
        for phase, (soil, temp, hum) in thresholds.items():
            c.execute('''INSERT OR REPLACE INTO irrigation_thresholds
                        (phase, soil_moisture_min, temperature_max, humidity_min)
                        VALUES (?, ?, ?, ?)''', (phase, soil, temp, hum))
        
        conn.commit()
        conn.close()

    def get_phenological_phase(self, device_id: str) -> str:
        """Obtiene la fase fenológica del dispositivo.
        Primero intenta obtenerla del Fog, si falla usa el caché local."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        try:
            # Intentar obtener nuevo valor del Fog
            print(f"Requesting phase from Fog for device {device_id}")
            response = requests.get(
                f"{self.base_url}/api/v1/devices/{device_id}/phase",
                timeout=5
            )
            print(f"Fog response: {response.status_code}")
            if response.status_code == 200:
                response_data = response.json()
                print(f"Fog response data: {response_data}")
                phase = response_data.get("phenologicalPhase")
                manually_active = response_data.get("manuallyActive", False)
                overwrite_automation = response_data.get("overwriteAutomation", False)
                # Actualizar el caché
                c.execute('''INSERT OR REPLACE INTO device_phases
                            (device_id, phenological_phase, last_updated, manually_active, overwrite_automation)
                            VALUES (?, ?, ?, ?, ?)''',
                         (device_id, phase, datetime.now(), manually_active, overwrite_automation))
                conn.commit()
                return phase
        except Exception as e:
            print(f"Error getting phenological phase from Fog: {e}")

        # Si falla, intentar obtener del caché
        c.execute('''SELECT phenological_phase FROM device_phases
                    WHERE device_id = ?''', (device_id,))
        result = c.fetchone()
        
        if result:
            return result[0]
        
        # Si no hay datos en caché, usar Germination como valor por defecto
        return "Germination"
        
    def get_irrigation_thresholds(self, phase: str) -> dict:
        """Obtiene los umbrales de riego para una fase específica"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT soil_moisture_min, temperature_max, humidity_min
                    FROM irrigation_thresholds WHERE phase = ?''', (phase,))
        result = c.fetchone()
        
        if result:
            return {
                "soil_moisture_min": result[0],
                "temperature_max": result[1],
                "humidity_min": result[2]
            }
        
        # Si no se encuentra la fase, devolver valores conservadores
        return {
            "soil_moisture_min": 60,  # Valor más alto para asegurar riego
            "temperature_max": 28,    # Valor más bajo para asegurar riego
            "humidity_min": 40        # Valor más alto para asegurar riego
        }
        
    def get_device_info(self, device_id: str) -> dict:
        """Obtiene la información completa del dispositivo desde el caché"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            # Intentar obtener nuevo valor del Fog
            response = requests.get(
                f"{self.base_url}/api/v1/devices/{device_id}/phase",
                timeout=5
            )
            if response.status_code == 200:
                response_data = response.json()
                phase = response_data.get("phenologicalPhase")
                manually_active = response_data.get("manuallyActive", False)
                overwrite_automation = response_data.get("overwriteAutomation", False)
                # Actualizar el caché
                c.execute('''INSERT OR REPLACE INTO device_phases
                            (device_id, phenological_phase, last_updated, manually_active, overwrite_automation)
                            VALUES (?, ?, ?, ?, ?)''',
                         (device_id, phase, datetime.now(), manually_active, overwrite_automation))
                conn.commit()
                return {
                    "phenological_phase": phase,
                    "manually_active": manually_active,
                    "overwrite_automation": overwrite_automation
                }
        except Exception as e:
            print(f"Error getting device info from Fog: {e}")

        # Si falla, intentar obtener del caché
        c.execute('''SELECT phenological_phase, manually_active, overwrite_automation
                    FROM device_phases WHERE device_id = ?''', (device_id,))
        result = c.fetchone()
        
        if result:
            return {
                "phenological_phase": result[0],
                "manually_active": bool(result[1]),
                "overwrite_automation": bool(result[2])
            }
        
        # Si no hay datos en caché, devolver valores por defecto
        return {
            "phenological_phase": "Germination",
            "manually_active": False,
            "overwrite_automation": False
        }