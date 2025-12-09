"""
Модуль sersors предоставляет абстракции для работы с данными сенсоров.
"""

from sensors.builtin.humidity import Humidity
from sensors.builtin.light import Light
from sensors.builtin.pressure import Pressure
from sensors.builtin.temperature import Temperature
from sensors.sensor import SensorValue

__all__ = [
    "SensorValue",
    "Temperature",
    "Humidity",
    "Pressure",
    "Light",
]


def hello() -> str:
    return "Hello from sensors!"
