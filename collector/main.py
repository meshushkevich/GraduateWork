import threading
from contextlib import asynccontextmanager

from collector_builtins.client.STM32 import STM32_FakeClient
from collector_builtins.sensor import GaussDistributedSensor, SeasonalSensor
from collector_core.mcu import MCU
from collector_daemon import CollectorDaemon
from fastapi import FastAPI

daemon = CollectorDaemon()


@asynccontextmanager
async def lifespan(app: FastAPI):
    daemon.clients.append(
        STM32_FakeClient(
            mcu=MCU(
                connection_type=MCU.MCU_ConnectionType.USB,
                is_connected=True,
                dev_id=302,
            ),
            sensors=[
                SeasonalSensor(name="temp0"),
                GaussDistributedSensor(name="temp1"),
            ],
        )
    )
    thread = threading.Thread(target=daemon.main_thread, daemon=True)
    thread.start()
    print("Daemon thread started")

    try:
        yield  # app runs here
    finally:
        # Thread is daemon=True, it will stop automatically when app exits
        print("Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.get("/ping")
def read_root():
    return {"message": "pong"}


@app.post("/add_mcu")
def add_mcu():
    daemon.add_mcu()
