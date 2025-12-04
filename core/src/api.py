import datetime
import logging
import os
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Load environment variables
def get_env_var(key, default=None):
    return os.environ.get(key, default)


# Initialize FastAPI app
app = FastAPI(
    title="Graduate Work Core API",
    description="Core API for communication between system components",
    version="0.1.0",
)

# Configure CORS
origins = get_env_var("CORS_ORIGINS", ["*"])
if isinstance(origins, str):
    # Handle comma-separated string from env
    origins = [origin.strip() for origin in origins.split(",")]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for data validation
class SensorData(BaseModel):
    sensor_id: str = Field(..., description="Unique identifier for the sensor")
    sensor_type: str = Field(
        ..., description="Type of sensor (temperature, humidity, etc.)"
    )
    value: float = Field(..., description="Sensor reading value")
    unit: str = Field(..., description="Unit of measurement")
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.now, description="Timestamp of the reading"
    )
    location: Optional[str] = Field(None, description="Location of the sensor")


class AlertConfig(BaseModel):
    alert_type: str = Field(..., description="Type of alert")
    threshold: float = Field(..., description="Threshold value")
    condition: str = Field(..., description="Condition to trigger alert (gt, lt, eq)")
    enabled: bool = Field(True, description="Whether the alert is enabled")
    recipients: List[str] = Field(
        default_factory=list, description="List of recipients for the alert"
    )


class PredictionRequest(BaseModel):
    prediction_type: str = Field(..., description="Type of prediction to make")
    parameters: Dict = Field(
        default_factory=dict, description="Parameters for the prediction model"
    )
    time_range: Optional[Dict] = Field(
        None, description="Time range for data to consider"
    )


# In-memory storage (replace with database in production)
sensor_data_store: Dict[str, List[SensorData]] = {}
alerts_store: Dict[str, AlertConfig] = {}
system_status = {
    "status": "online",
    "start_time": datetime.datetime.now(),
    "active_sensors": 0,
    "last_data_update": None,
}


# API Routes
@app.get("/")
async def root():
    """Root endpoint with basic API information"""
    return {
        "message": "Graduate Work Core API",
        "status": "online",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "sensor_data": "/sensor_data",
            "alerts": "/alerts",
            "predictions": "/predictions",
            "status": "/status",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.datetime.now()}


# Sensor data endpoints
@app.post("/sensor_data")
async def receive_sensor_data(data: SensorData):
    """Receive and store sensor data"""
    logger.info(f"Received data from sensor: {data.sensor_id}")

    # Store the data
    if data.sensor_id not in sensor_data_store:
        sensor_data_store[data.sensor_id] = []

    sensor_data_store[data.sensor_id].append(data)

    # Update system status
    system_status["last_data_update"] = data.timestamp

    # Check for alerts (simplified logic for demonstration)
    for alert_id, alert in alerts_store.items():
        if alert.enabled:
            if (
                (alert.condition == "gt" and data.value > alert.threshold)
                or (alert.condition == "lt" and data.value < alert.threshold)
                or (alert.condition == "eq" and data.value == alert.threshold)
            ):
                logger.warning(
                    f"Alert triggered: {alert_id} - {data.value} {data.unit}"
                )
                # In a real system, this would send notifications

    return {
        "status": "success",
        "message": f"Data received from sensor {data.sensor_id}",
    }


@app.get("/sensor_data")
async def get_sensor_data(
    sensor_id: Optional[str] = Query(None, description="Filter by sensor ID"),
    sensor_type: Optional[str] = Query(None, description="Filter by sensor type"),
    limit: int = Query(100, description="Maximum number of records to return", le=1000),
):
    """Retrieve stored sensor data with optional filters"""
    result = []

    for s_id, data_list in sensor_data_store.items():
        if sensor_id and s_id != sensor_id:
            continue

        for data in data_list:
            if sensor_type and data.sensor_type != sensor_type:
                continue

            result.append(data)

            if len(result) >= limit:
                return {"data": result}

    return {"data": result}


@app.get("/sensor_data/{sensor_id}")
async def get_sensor_data_by_id(sensor_id: str = Path(..., description="Sensor ID")):
    """Retrieve data for a specific sensor"""
    if sensor_id not in sensor_data_store:
        raise HTTPException(status_code=404, detail=f"Sensor {sensor_id} not found")

    return {"sensor_id": sensor_id, "data": sensor_data_store[sensor_id]}


# Alert management endpoints
@app.post("/alerts")
async def create_alert(alert_id: str, alert: AlertConfig):
    """Create a new alert configuration"""
    alerts_store[alert_id] = alert
    logger.info(f"Created alert: {alert_id}")
    return {"status": "success", "message": f"Alert {alert_id} created"}


@app.get("/alerts")
async def get_alerts():
    """Retrieve all alert configurations"""
    return {"alerts": alerts_store}


@app.delete("/alerts/{alert_id}")
async def delete_alert(alert_id: str = Path(..., description="Alert ID")):
    """Delete an alert configuration"""
    if alert_id not in alerts_store:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")

    del alerts_store[alert_id]
    logger.info(f"Deleted alert: {alert_id}")
    return {"status": "success", "message": f"Alert {alert_id} deleted"}


# Prediction endpoints
@app.post("/predictions")
async def request_prediction(request: PredictionRequest):
    """Request a prediction from the predictor module"""
    logger.info(f"Prediction requested: {request.prediction_type}")

    # In a real implementation, this would call the predictor module
    # Here we just return a placeholder response
    return {
        "status": "success",
        "prediction_type": request.prediction_type,
        "result": "Prediction placeholder result",
        "confidence": 0.95,
        "timestamp": datetime.datetime.now(),
    }


# System status endpoints
@app.get("/status")
async def get_system_status():
    """Get overall system status"""
    uptime = (datetime.datetime.now() - system_status["start_time"]).total_seconds()
    active_sensors = len(sensor_data_store)

    return {
        "status": system_status["status"],
        "uptime_seconds": uptime,
        "active_sensors": active_sensors,
        "total_data_points": sum(len(data) for data in sensor_data_store.values()),
        "active_alerts": sum(1 for alert in alerts_store.values() if alert.enabled),
        "last_data_update": system_status["last_data_update"],
    }


# Collector integration endpoints
@app.post("/collector/status")
async def update_collector_status(status: Dict):
    """Receive status updates from the collector module"""
    logger.info(f"Collector status update: {status}")
    return {"status": "received"}


# Predictor integration endpoints
@app.post("/predictor/result")
async def receive_prediction_result(result: Dict):
    """Receive prediction results from the predictor module"""
    logger.info(f"Received prediction result: {result}")
    # In a real implementation, this would store or act on the prediction
    return {"status": "success"}


if __name__ == "__main__":
    # Configuration from environment variables with defaults
    host = get_env_var("CORE_API_HOST", "0.0.0.0")
    port = int(get_env_var("CORE_API_PORT", "8000"))
    debug = get_env_var("CORE_API_DEBUG", "false").lower() == "true"
    reload = get_env_var("CORE_API_RELOAD", "true").lower() == "true"

    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=reload,
        log_level="debug" if debug else "info",
    )
