from dataclasses import dataclass

import numpy as np
from collector_core.sensor import SensorBase


@dataclass
class GaussDistributedSensor(SensorBase):
    mean: float = 0.0
    sigma: float = 1.0

    def read(self) -> float:
        return np.random.normal(self.mean, self.sigma)
