import asyncio
import pprint

from collector_core.client import AsyncClientBase
from collector_core.db import init_db

from collector_daemon.logger import log_debug, log_info


class CollectorDaemon:
    clients: list[AsyncClientBase]
    queue: asyncio.Queue = asyncio.Queue()

    def __init__(self):
        self.clients = []
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
                for sensor in await client.get_list_of_sensors_names():
                    log_info(f"GED {sensor} -> {client.mcu.dev_id}")
                    data = await client.get_sensor_data(sensor)
                    await self.queue.put(
                        {"dev_id": client.mcu.dev_id, "sensor": sensor, "data": data}
                    )
                    log_info(f"GED {sensor}:{data:.2f} <- {client.mcu.dev_id}")
                    await asyncio.sleep(1)

    async def task_send_data(self):
        while True:
            data = await self.queue.get()
            log_info("=" * 32)
            for line in pprint.pformat(data).splitlines():
                log_info(line)
