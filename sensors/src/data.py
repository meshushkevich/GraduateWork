from pydantic import BaseModel


class SensorData(BaseModel):
    fingerprint: str
    mcu_name: str
    sensor_name: str
    value: float
    timestamp: float
