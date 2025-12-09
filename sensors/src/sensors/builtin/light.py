from dataclasses import dataclass

from sensors.sensor import SensorValue


@dataclass
class Light(SensorValue):
    value: float
    unit: str = "lux"

    @property
    def sensor_type(self) -> str:
        return "light"
