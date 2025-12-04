from dataclasses import dataclass

from sensors.sensor import SensorValue


@dataclass
class Light(SensorValue):
    """Сенсор освещенности"""

    value: float
    unit: str = "lux"  # Единицы измерения (люксы)

    @property
    def sensor_type(self) -> str:
        return "light"
