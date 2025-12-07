from dataclasses import dataclass

import numpy as np

from collector.mock_sensor.sensor_base import SensorBase


@dataclass
class CosineSensor(SensorBase):
    amplitude: float = 1.0
    period: float = 100
    noise: float = 0.05
    drift_scale: float = 0.0002

    _t: int = 0
    _drift: float = 0.0

    def read(self) -> float:
        base = self.amplitude * np.cos(2 * np.pi * self.t / self.period)
        noise = np.random.normal(scale=self.noise)
        self.drift += np.random.normal(scale=self.drift_scale)
        value = base + noise + self.drift
        self.t += 1
        return float(value)
