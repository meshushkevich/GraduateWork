import random
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Type

import requests

from sensors import Humidity, Light, Pressure, SensorValue, Temperature


class SensorSimulator:
    """Класс для симуляции данных сенсоров и отправки их в Core API"""

    def __init__(
        self, api_url: str = "http://localhost:8000", api_key: Optional[str] = None
    ):
        """
        Инициализация симулятора сенсоров

        Args:
            api_url: URL Core API
            api_key: Опциональный ключ для аутентификации
        """
        self.api_url = api_url
        self.api_key = api_key
        self.sensor_configs: List[Dict[str, Any]] = []

    def add_sensor_config(
        self,
        sensor_type: Type[SensorValue],
        sensor_id: str,
        min_value: float,
        max_value: float,
        jitter: float = 0.1,
        trend: float = 0.0,
    ) -> None:
        """
        Добавляет конфигурацию для сенсора

        Args:
            sensor_type: Тип сенсора (класс)
            sensor_id: Уникальный идентификатор сенсора
            min_value: Минимальное значение для генерации
            max_value: Максимальное значение для генерации
            jitter: Разброс значений (доля от диапазона)
            trend: Тренд изменения значения (положительный/отрицательный)
        """
        config = {
            "sensor_type": sensor_type,
            "sensor_id": sensor_id,
            "min_value": min_value,
            "max_value": max_value,
            "jitter": jitter,
            "trend": trend,
            "current_value": random.uniform(min_value, max_value),
        }
        self.sensor_configs.append(config)

    def _generate_sensor_value(self, config: Dict[str, Any]) -> SensorValue:
        """Генерирует случайное значение сенсора с учетом настроек"""
        # Вычисляем диапазон и тренд
        value_range = config["max_value"] - config["min_value"]
        trend_step = value_range * config["trend"]
        jitter_range = value_range * config["jitter"]

        # Обновляем текущее значение с трендом и разбросом
        new_value = (
            config["current_value"]
            + trend_step
            + random.uniform(-jitter_range, jitter_range)
        )

        # Ограничиваем значение в допустимых пределах
        new_value = max(config["min_value"], min(config["max_value"], new_value))

        # Сохраняем новое текущее значение
        config["current_value"] = new_value

        # Создаем экземпляр сенсора
        sensor_class = config["sensor_type"]
        return sensor_class(value=new_value)

    def collect_and_send_data(self) -> None:
        """Собирает данные со всех сенсоров и отправляет их в API"""
        for config in self.sensor_configs:
            sensor_data = self._generate_sensor_value(config)
            self._send_to_api(config["sensor_id"], sensor_data)

    def _send_to_api(self, sensor_id: str, sensor_data: SensorValue) -> None:
        """Отправляет данные сенсора в Core API"""
        url = f"{self.api_url}/sensor_data"

        # Подготавливаем payload для API
        payload = {
            "sensor_id": sensor_id,
            "sensor_type": sensor_data.sensor_type,
            "value": sensor_data.value,
            "unit": sensor_data.unit,
            "timestamp": sensor_data.timestamp.isoformat(),
        }

        headers = self._get_headers()

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                print(f"Successfully sent data from sensor {sensor_id}")
            else:
                print(
                    f"Failed to send data from sensor {sensor_id}: {response.status_code} - {response.text}"
                )
        except Exception as e:
            print(f"Error sending data from sensor {sensor_id}: {str(e)}")

    def _get_headers(self) -> Dict[str, str]:
        """Возвращает заголовки для запроса к API"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def run_simulation(
        self, interval_seconds: int = 5, duration_seconds: Optional[int] = None
    ) -> None:
        """
        Запускает симуляцию данных сенсоров

        Args:
            interval_seconds: Интервал между отправками данных в секундах
            duration_seconds: Длительность симуляции (None - бесконечно)
        """
        print(f"Starting sensor simulation with {len(self.sensor_configs)} sensors...")

        start_time = time.time()
        try:
            while True:
                self.collect_and_send_data()

                # Проверяем, не истекло ли время симуляции
                if duration_seconds and (time.time() - start_time) >= duration_seconds:
                    break

                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\nSimulation stopped by user.")


def create_default_simulator() -> SensorSimulator:
    """Создает симулятор с конфигурациями сенсоров по умолчанию"""
    simulator = SensorSimulator()

    # Конфигурации различных сенсоров
    simulator.add_sensor_config(
        sensor_type=Temperature,
        sensor_id="temp_server_room_01",
        min_value=18.0,
        max_value=28.0,
        jitter=0.05,
    )

    simulator.add_sensor_config(
        sensor_type=Humidity,
        sensor_id="hum_server_room_01",
        min_value=30.0,
        max_value=60.0,
        jitter=0.1,
    )

    simulator.add_sensor_config(
        sensor_type=Pressure,
        sensor_id="pressure_server_room_01",
        min_value=990.0,
        max_value=1050.0,
        jitter=0.01,
    )

    simulator.add_sensor_config(
        sensor_type=Light,
        sensor_id="light_server_room_01",
        min_value=50.0,
        max_value=800.0,
        jitter=0.2,
    )

    # Сенсор с растущей температурой (для тестирования алертов)
    simulator.add_sensor_config(
        sensor_type=Temperature,
        sensor_id="temp_critical_01",
        min_value=20.0,
        max_value=35.0,
        jitter=0.02,
        trend=0.01,  # Небольшой рост температуры
    )

    return simulator


if __name__ == "__main__":
    # Создаем и запускаем симулятор по умолчанию
    simulator = create_default_simulator()

    # Запускаем симуляцию с интервалом 5 секунд
    simulator.run_simulation(interval_seconds=5)
