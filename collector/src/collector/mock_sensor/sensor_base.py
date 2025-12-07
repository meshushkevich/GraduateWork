from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SensorBase(ABC):
    name: str

    @abstractmethod
    def read(self) -> float:
        raise NotImplementedError
