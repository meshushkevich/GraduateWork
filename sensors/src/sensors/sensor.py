from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict


@dataclass
class SensorValue(ABC):
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    unit: str = "unknown"

    @property
    @abstractmethod
    def sensor_type(self) -> str:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sensor_type": self.sensor_type,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat(),
        }
