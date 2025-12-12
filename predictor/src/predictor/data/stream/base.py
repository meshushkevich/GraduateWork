from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from typing import Optional

from sensors.data import SensorData


@dataclass
class DataStream(ABC):
    _available_data: deque[SensorData] = field(default_factory=deque)

    _fingerprint: str = "0xdeadbeef"
    _mcu_dev_id: int = 0
    _sensor_name: str = "unknown"

    def set_triple(self, fingerprint: str, mcu_dev_id: int, sensor_name: str):
        self._fingerprint = fingerprint
        self._mcu_dev_id = mcu_dev_id
        self._sensor_name = sensor_name

    def __len__(self) -> int:
        return len(self._available_data)

    def pop(self, horizont: int) -> Optional[tuple[list[float], float]]:
        if horizont + 1 > len(self._available_data):
            return

        data_X = [self._available_data[i].value for i in range(horizont)]
        data_Y = self._available_data[horizont].value
        self._available_data.popleft()
        return data_X, data_Y

    def get_batches(
        self, num_batches: int, horizont: int
    ) -> tuple[list[list[float]], list[float]]:
        batch_x: list[list[float]] = []
        batch_y: list[float] = []
        while len(batch_x) < num_batches:
            if batch := self.pop(horizont):
                x, y = batch
                batch_x.append(x)
                batch_y.append(y)
            else:
                self.update(horizont)
        return batch_x, batch_y

    @abstractmethod
    def update(self, horizont: int):
        raise NotImplementedError

    def add_data(self, data: SensorData):
        if data.fingerprint != self._fingerprint:
            raise ValueError("Fingerprint mismatch")
        if data.mcu_dev_id != self._mcu_dev_id:
            raise ValueError("MCU ID mismatch")
        if data.sensor_name != self._sensor_name:
            raise ValueError("Sensor name mismatch")
        self._available_data.append(data)
