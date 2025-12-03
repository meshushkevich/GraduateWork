from dataclasses import dataclass

from sensors.sensor import SensorValue


@dataclass
class Temperature(SensorValue):
    value: float
