from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class SensorValue(ABC):
    """
    """Абстрактный базовый класс для значений сенсоров.
    Каждый конкретный сенсор должен наследовать этот класс.
    """

    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    unit: str = "unknown"

    @property
    @abstractmethod
    def sensor_type(self) -> str:
        """Возвращает тип сенсора"""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует значение сенсора в словарь"""
        return {
            "sensor_type": self.sensor_type,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat(),
        }
