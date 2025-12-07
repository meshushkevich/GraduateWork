from dataclasses import dataclass

from sensors.sensor import SensorValue


@dataclass
class Humidity(SensorValue):
    value: float
    unit: str = "%"

    @property
    def sensor_type(self) -> str:
        return "humidity"
