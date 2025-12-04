from dataclasses import dataclass

from sensors.sensor import SensorValue


@dataclass
class Humidity(SensorValue):
    """Сенсор влажности"""

    value: float
    unit: str = "%"  # Единицы измерения

    @property
    def sensor_type(self) -> str:
        return "humidity"
