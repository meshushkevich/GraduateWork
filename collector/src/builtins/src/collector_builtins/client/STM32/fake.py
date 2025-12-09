from dataclasses import dataclass, field
from typing import Optional

from collector_core.client import AsyncClientBase
from collector_core.sensor import SensorBase


@dataclass
class STM32_FakeClient(AsyncClientBase):
    sensors: list = field(default_factory=list)

    async def get_heartbeat(self) -> bool:
        return True

    async def get_mcu_name(self) -> str:
        return self.mcu.name

    async def get_mcu_dev_id(self) -> int:
        return self.mcu.dev_id

    async def get_mcu_info(self) -> str:
        return "This is a fake MCU"

    async def get_list_of_sensors_names(self) -> list[str]:
        return [sensor.name for sensor in self.sensors]

    async def get_sensor_data(self, sensor_name: str) -> float:
        for sensor in self.sensors:
            if sensor.name == sensor_name:
                return sensor.read()
        return 0.0

    # Fake specific settings
    def add_sensor(self, sensor: SensorBase) -> Optional[str]:
        if all(sensor.name not in self.sensors for sensor in self.sensors):
            self.sensors.append(sensor)
        return f"There is a sensor with the same name: {sensor.name}"
