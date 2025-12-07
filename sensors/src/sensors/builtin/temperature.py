from dataclasses import dataclass

from sensors.sensor import SensorValue


@dataclass
class Temperature(SensorValue):
    """Сенсор температуры"""

    value: float
    unit: str = "°C"  # Единицы измерения

    @property
    def sensor_type(self) -> str:
        return "temperature"
