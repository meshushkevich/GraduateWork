import datetime
import time
from pathlib import Path

import pandas as pd
from sensors.data import SensorData

from predictor import PROJECT_ROOT
from predictor.data.stream.base import DataStream

DEFAULT_DATASET_PATH = PROJECT_ROOT / "datasets" / "SHT" / "train.csv"
SENSORS = [
    "CO2_(dinning-room)",
    "CO2_room",
    "Relative_humidity_(dinning-room)",
    "Relative_humidity_room",
    "Lighting_(dinning-room)",
    "Lighting_room",
    "Meteo_Rain",
    "Meteo_Sun_dusk",
    "Meteo_Wind",
    "Meteo_Sun_light_in_west_facade",
    "Meteo_Sun_light_in_east_facade",
    "Meteo_Sun_light_in_south_facade",
    "Meteo_Sun_irradiance",
    "Outdoor_relative_humidity_Sensor",
    "Day_of_the_week",
    "Indoor_temperature_room",
]


class SmartHomesTempDatastream(DataStream):
    def __init__(
        self,
        period_for_sample_ms: float = 1.0,
        sensor_name: str = "CO2_room",
        csv_path: Path = DEFAULT_DATASET_PATH,
    ):
        super().__init__(_sensor_name=sensor_name)
        self._period = period_for_sample_ms
        self._last_update_time = 0.0

        self._dataset = pd.read_csv(csv_path)
        self._index = 0

    def update(self, horizont: int):
        current_time_ms = time.time() * 1000
        delta = current_time_ms - self._last_update_time
        if delta < self._period:
            return
        self._last_update_time = current_time_ms
        if self._index + horizont > len(self._dataset):
            self._index = 0
        if len(self._dataset) < horizont:
            return

        timestamp = datetime.datetime.now()
        for shift in range(horizont):
            row = self._dataset.iloc[self._index + shift]
            data = SensorData(
                fingerprint=self._fingerprint,
                mcu_dev_id=self._mcu_dev_id,
                sensor_name=self._sensor_name,
                value=row[self._sensor_name],
                timestamp=timestamp,
            )
            self.add_data(data)

        self._index = (self._index + horizont) % len(self._dataset)
