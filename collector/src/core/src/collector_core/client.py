from abc import ABC, abstractmethod
from dataclasses import dataclass

from collector_core.mcu import MCU


@dataclass
class AsyncClientBase(ABC):
    mcu: MCU

    @abstractmethod
    async def get_heartbeat(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_mcu_info(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_list_of_sensors_names(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    async def get_sensor_data(self, sensor_name: str) -> float:
        raise NotImplementedError
