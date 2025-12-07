import random
from dataclasses import dataclass

from collector_core.sensor import SensorBase


@dataclass
class ConstantSensor(SensorBase):
    target_value: float = 0.0
    noise: float = 0.0

    def read(self) -> float:
        return self.target_value + self.noise * random.random()
