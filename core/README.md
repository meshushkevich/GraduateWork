# Graduate Work Core API

The Core API serves as the central communication hub between system components, including sensors, data collectors, predictors, and alerting systems.

## Features

- RESTful API built with FastAPI
- In-memory data storage (can be replaced with a database)
- Automatic documentation generation
- CORS support for frontend integration
- Real-time sensor data reception
- Alert configuration and management
- Prediction request handling
- System status monitoring

## Installation

```bash
# Install dependencies
pip install -e .

# Run the API server
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

#### General Endpoints

##### GET `/`
Root endpoint with basic API information.

##### GET `/health`
Health check endpoint.

#### Sensor Data Endpoints

##### POST `/sensor_data`
Receive and store sensor data from any sensor module.

**Request Body:**
```json
{
  "sensor_id": "temp_sensor_01",
  "sensor_type": "temperature",
  "value": 23.5,
  "unit": "celsius",
  "timestamp": "2023-11-15T14:30:00",
  "location": "room_1"
}
```

##### GET `/sensor_data`
Retrieve stored sensor data with optional filters.

**Query Parameters:**
- `sensor_id` (optional): Filter by sensor ID
- `sensor_type` (optional): Filter by sensor type
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**
```json
{
  "data": [
    {
      "sensor_id": "temp_sensor_01",
      "sensor_type": "temperature",
      "value": 23.5,
      "unit": "celsius",
      "timestamp": "2023-11-15T14:30:00",
      "location": "room_1"
    }
  ]
}
```

##### GET `/sensor_data/{sensor_id}`
Retrieve data for a specific sensor.

#### Alert Management Endpoints

##### POST `/alerts`
Create a new alert configuration.

**Request Body:**
```json
{
  "alert_type": "high_temperature",
  "threshold": 30.0,
  "condition": "gt",
  "enabled": true,
  "recipients": ["admin@example.com"]
}
```

##### GET `/alerts`
Retrieve all alert configurations.

##### DELETE `/alerts/{alert_id}`
Delete an alert configuration.

#### Prediction Endpoints

##### POST `/predictions`
Request a prediction from the predictor module.

**Request Body:**
```json
{
  "prediction_type": "temperature_forecast",
  "parameters": {
    "hours_ahead": 24
  },
  "time_range": {
    "start": "2023-11-15T00:00:00",
    "end": "2023-11-16T00:00:00"
  }
}
```

#### System Status Endpoints

##### GET `/status`
Get overall system status.

**Response:**
```json
{
  "status": "online",
  "uptime_seconds": 3600,
  "active_sensors": 5,
  "total_data_points": 1000,
  "active_alerts": 3,
  "last_data_update": "2023-11-15T14:30:00"
}
```

#### Integration Endpoints

##### POST `/collector/status`
Receive status updates from the collector module.

##### POST `/predictor/result`
Receive prediction results from the predictor module.

## Data Models

### SensorData
```python
class SensorData(BaseModel):
    sensor_id: str
    sensor_type: str
    value: float
    unit: str
    timestamp: datetime.datetime
    location: Optional[str] = None
```

### AlertConfig
```python
class AlertConfig(BaseModel):
    alert_type: str
    threshold: float
    condition: str  # "gt", "lt", "eq"
    enabled: bool = True
    recipients: List[str] = []
```

### PredictionRequest
```python
class PredictionRequest(BaseModel):
    prediction_type: str
    parameters: Dict = {}
    time_range: Optional[Dict] = None
```

## Example Usage

### Sending Sensor Data
```python
import requests

data = {
    "sensor_id": "temp_sensor_01",
    "sensor_type": "temperature",
    "value": 23.5,
    "unit": "celsius",
    "location": "room_1"
}

response = requests.post("http://localhost:8000/sensor_data", json=data)
print(response.json())
```

### Creating an Alert
```python
import requests

alert = {
    "alert_type": "high_temperature",
    "threshold": 30.0,
    "condition": "gt",
    "enabled": True,
    "recipients": ["admin@example.com"]
}

response = requests.post(f"http://localhost:8000/alerts?", params={"alert_id": "temp_alert_01"}, json=alert)
print(response.json())
```

### Requesting a Prediction
```python
import requests

prediction_request = {
    "prediction_type": "temperature_forecast",
    "parameters": {
        "hours_ahead": 24
    }
}

response = requests.post("http://localhost:8000/predictions", json=prediction_request)
print(response.json())
```

## Development

To run with hot reload during development:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

For production, consider:

1. Using a proper database instead of in-memory storage
2. Implementing authentication and authorization
3. Configuring proper CORS settings instead of wildcard
4. Setting up monitoring and logging
5. Using a process manager like Gunicorn or Uvicorn with multiple workers

## Integration with Other Modules

The Core API is designed to integrate with:

- **Collector Module**: Receives data collectors status updates via `/collector/status`
- **Predictor Module**: Receives prediction results via `/predictor/result`
- **Sensor Modules**: Receive data via `/sensor_data`
- **Alarm Module**: Triggers alerts based on configured thresholds