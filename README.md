# WaruSmart - Edge Application

Aplicación backend de borde para **WaruSmart**, un sistema inteligente de monitoreo y control de riego agrícola basado en IoT.

---

## ⚙️ Setup del Proyecto Local

###  Ejecutar la aplicación

python app.py

La aplicación correrá en `http://localhost:5000`

---

## 🌐 Configuración con ngrok

Para exponer tu aplicación local a dispositivos externos:

### 1. Descargar ngrok

[https://ngrok.com/download](https://ngrok.com/download)

### 2. Ejecutar ngrok (en terminal separada)

```bash
ngrok http --scheme=http 5000
```

### 3. Copiar URL pública

Verás algo como:
```
Forwarding    http://abc1234def56-us.ngrok.io -> http://localhost:5000
```

Usa `http://abc1234def56-us.ngrok.io` en tus solicitudes.

---

## 🔌 Endpoints de API

### 1. POST `/api/v1/monitoring/device-metrics`

Registra nuevas métricas de sensores.

**Headers:**
```
Content-Type: application/json
X-API-Key: test-api-key-123
```

**Body:**
```json
{
  "device_id": "waru-smart-001",
  "zone": "zona-norte",
  "soil_moisture": 65.5,
  "temperature": 28.3,
  "humidity": 72.1,
  "created_at": "2025-11-16T14:30:00Z"
}
```

**Ejemplo con ngrok:**
```bash
curl -X POST http://abc1234def56-us.ngrok.io/api/v1/monitoring/device-metrics \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key-123" \
  -d '{
    "device_id": "waru-smart-001",
    "zone": "zona-norte",
    "soil_moisture": 65.5,
    "temperature": 28.3,
    "humidity": 72.1
  }'
```

**Respuesta (201):**
```json
{
  "device_id": "waru-smart-001",
  "zone": "zona-norte",
  "soil_moisture": 65.5,
  "temperature": 28.3,
  "humidity": 72.1,
  "created_at": "2025-11-16T14:30:00Z"
}
```

---

### 2. POST `/api/v1/device-config`

Actualiza configuración de umbrales.

**Headers:**
```
Content-Type: application/json
X-API-Key: test-api-key-123
```

**Body:**
```json
{
  "device_id": "waru-smart-001",
  "parcela_id": "parcela-001",
  "soil_moisture_min_device": 50.0,
  "temperature_max_device": 30.0,
  "humidity_min_device": 35.0,
  "overwrite_automation": false,
  "manually_active": false
}
```

**Ejemplo con ngrok:**
```bash
curl -X POST http://abc1234def56-us.ngrok.io/api/v1/device-config \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key-123" \
  -d '{
    "device_id": "waru-smart-001",
    "parcela_id": "parcela-001",
    "soil_moisture_min_device": 50.0,
    "temperature_max_device": 30.0,
    "humidity_min_device": 35.0,
    "overwrite_automation": false,
    "manually_active": false
  }'
```

**Respuesta (200):**
```json
{
  "message": "Configuración actualizada correctamente",
  "device_id": "waru-smart-001",
  "parcela_id": "parcela-001",
  "soil_moisture_min_device": 50.0,
  "temperature_max_device": 30.0,
  "humidity_min_device": 35.0,
  "overwrite_automation": false,
  "manually_active": false,
  "updated_at": "2025-11-16T14:35:00Z"
}
```

---

### 3. GET `/sensor`

Obtiene datos más recientes de sensores.

**Query Parameters:**
```
device_id=waru-smart-001 (opcional)
```

**Ejemplo con ngrok:**
```bash
curl http://abc1234def56-us.ngrok.io/sensor?device_id=waru-smart-001
```

**Respuesta (200):**
```json
{
  "device": {
    "deviceId": "waru-smart-001",
    "zone": "zona-norte",
    "parcela_id": "parcela-001"
  },
  "current_metrics": {
    "soil_moisture": 65.5,
    "temperature": 28.3,
    "humidity": 72.1,
    "timestamp": "2025-11-16T14:30:00Z"
  },
  "device_config": {
    "thresholds": {
      "soil_moisture_min": 50.0,
      "temperature_max": 30.0,
      "humidity_min": 35.0
    },
    "automation": {
      "overwrite_automation": false,
      "manually_active": false
    }
  },
  "actuator_status": {
    "status": "active",
    "type": "valve"
  }
}
```

---

## 📡 Headers Requeridos

| Header | Valor | Requerido |
|--------|-------|-----------|
| `Content-Type` | `application/json` | ✅ (POST) |
| `X-API-Key` | `test-api-key-123` | ✅ (POST) |

---

## � Credenciales de Prueba

- **Device ID**: `test-device-123`
- **API Key**: `test-api-key-123`
