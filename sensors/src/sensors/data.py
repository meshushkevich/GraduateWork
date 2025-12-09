from datetime import datetime

from pydantic import BaseModel


class SensorData(BaseModel):
    fingerprint: str
    mcu_dev_id: int
    sensor_name: str
    value: float
    timestamp: int
