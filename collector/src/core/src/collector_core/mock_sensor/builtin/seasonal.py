from dataclasses import dataclass

import numpy as np

from collector.mock_sensor.sensor_base import SensorBase


@dataclass
class SeasonalSensor(SensorBase):
    ar_coeff: float = 0.90
    noise_scale: float = 0.2
    drift_scale: float = 0.0005
    trend_rate: float = 0.0001

    fast_period: float = 60
    slow_period: float = 1440
    adc_step: float = 0.01

    _t: int = 0
    _noise_prev: float = 0.0
    _drift: float = 0.0

    def read(self):
        t = self._t

        trend = self.trend_rate * t
        seasonal = 1.0 * np.sin(2 * np.pi * t / self.slow_period) + 0.3 * np.sin(
            2 * np.pi * t / self.fast_period
        )
        eps = np.random.normal(scale=self.noise_scale)
        noise = self.ar_coeff * self._noise_prev + eps
        self._noise_prev = noise

        self._drift += np.random.normal(scale=self.drift_scale)

        value = 10.0 + trend + seasonal + noise + self._drift

        if np.random.random() < 0.001:  # 0.1%
            value += np.random.normal(loc=5, scale=3)

        value = round(value / self.adc_step) * self.adc_step
        self._t += 1
        return float(value)
