from collector_core.client import AsyncClientBase


class STM32_RealClient(AsyncClientBase):
    async def get_heartbeat(self) -> bool:
        raise NotImplementedError

    async def get_mcu_name(self) -> str:
        raise NotImplementedError

    async def get_mcu_dev_id(self) -> int:
        raise NotImplementedError

    async def get_mcu_info(self) -> str:
        raise NotImplementedError

    async def get_list_of_sensors(self) -> list[str]:
        raise NotImplementedError

    async def get_sensor_data(self, sensor_name: str) -> float:
        raise NotImplementedError
