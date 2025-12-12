import asyncio
import os
from datetime import datetime

import requests
from collector_core.client import AsyncClientBase
from collector_core.db import init_db
from collector_core.fingerprint import get_machine_fingerprint
from sensors.data import SensorData

from collector_daemon.logger import log_debug, log_info


class CollectorDaemon:
    clients: list[AsyncClientBase]
    queue: asyncio.Queue = asyncio.Queue()

    def __init__(self):
        self.clients = []
        self.fingerprint = get_machine_fingerprint()
        self.api_url = os.getenv("API_URL", "http://core:8000")
        init_db()

    def main_thread(self):
        asyncio.run(self._entrypoint())

    async def _entrypoint(self):
        t1 = asyncio.create_task(self.task_heartbeat())
        t2 = asyncio.create_task(self.task_collect())
        t3 = asyncio.create_task(self.task_send_data())
        await asyncio.gather(t1, t2, t3)

    async def task_heartbeat(self):
        while True:
            log_info("Starting heartbeat loop")
            for client in self.clients:
                log_info(f"Heartbeat -> {client.mcu.dev_id}")
                await client.get_heartbeat()
            await asyncio.sleep(5)

    async def task_collect(self):
        while True:
            log_info("Starting collect loop")
            for client in self.clients:
                for sensor_name in await client.get_list_of_sensors_names():
                    value = await client.get_sensor_data(sensor_name)
                    data = SensorData(
                        fingerprint=self.fingerprint,
                        mcu_dev_id=client.mcu.dev_id,
                        sensor_name=sensor_name,
                        value=value,
                        timestamp=datetime.now(),
                    )
                    await self.queue.put(data)
                    await asyncio.sleep(1)

    async def task_send_data(self):
        while True:
            data: SensorData = await self.queue.get()
            result = requests.post(
                url=f"{self.api_url}/data",
                data=data.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            if result.status_code == 200:
                log_debug("Data sent successfully")
            else:
                log_debug("Failed to send data")
