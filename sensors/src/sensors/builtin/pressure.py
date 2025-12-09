from dataclasses import dataclass

from sensors.sensor import SensorValue


@dataclass
class Pressure(SensorValue):
    """Сенсор давления"""

    value: float
    unit: str = "hPa"  # Единицы измерения (гектопаскали)

    @property
    def sensor_type(self) -> str:
        return "pressure"
