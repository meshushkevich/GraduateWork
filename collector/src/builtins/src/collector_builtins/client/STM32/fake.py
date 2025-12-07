from typing import Optional

from collector_core.client import AsyncClientBase
from collector_core.sensor import SensorBase


class FakeClient(AsyncClientBase):
    sensors: list

    async def get_heartbeat(self) -> bool:
        return True

    async def get_mcu_info(self) -> str:
        return "This is a fake MCU"

    async def get_list_of_sensors(self) -> list[str]:
        return self.sensors

    async def get_sensor_data(self, sensor_name: str) -> float:
        return 0.0

    # Fake specific settings
    def add_sensor(self, sensor: SensorBase) -> Optional[str]:
        if all(sensor.name not in self.sensors for sensor in self.sensors):
            self.sensors.append(sensor)
        return f"There is a sensor with the same name: {sensor.name}"
