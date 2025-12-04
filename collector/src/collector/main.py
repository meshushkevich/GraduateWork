import argparse

from collector.imitator.sensor_simulator import (
    SensorSimulator,
    create_default_simulator,
)


def main():
    parser = argparse.ArgumentParser(description="Симулятор данных сенсоров")
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000",
        help="URL Core API (по умолчанию: http://localhost:8000)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Интервал между отправками данных в секундах (по умолчанию: 5)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=None,
        help="Длительность симуляции в секундах (по умолчанию: бесконечно)",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="API ключ для аутентификации",
    )
    parser.add_argument(
        "--custom",
        action="store_true",
        help="Использовать пользовательскую конфигурацию сенсоров",
    )

    args = parser.parse_args()

    print("Запуск симулятора данных сенсоров...")
    print(f"API URL: {args.api_url}")
    print(f"Интервал: {args.interval} сек")
    print(
        f"Длительность: {args.duration} сек"
        if args.duration
        else "Длительность: бесконечно"
    )

    if args.custom:
        # Создаем пустой симулятор для пользовательской конфигурации
        simulator = SensorSimulator(api_url=args.api_url, api_key=args.api_key)
        add_custom_sensors(simulator)
        print("Используется пользовательская конфигурация сенсоров")
    else:
        # Используем симулятор с настройками по умолчанию
        simulator = create_default_simulator()
        simulator.api_url = args.api_url
        simulator.api_key = args.api_key
        print("Используется конфигурация сенсоров по умолчанию")

    try:
        simulator.run_simulation(
            interval_seconds=args.interval, duration_seconds=args.duration
        )
    except KeyboardInterrupt:
        print("\nСимуляция остановлена пользователем")
    except Exception as e:
        print(f"Ошибка при запуске симуляции: {str(e)}")


def add_custom_sensors(simulator: SensorSimulator):
    """Добавляет пользовательскую конфигурацию сенсоров (пример для тестирования)"""
    from sensors import Humidity, Temperature

    # Добавление пользовательских сенсоров
    simulator.add_sensor_config(
        sensor_type=Temperature,
        sensor_id="temp_office_01",
        min_value=20.0,
        max_value=25.0,
        jitter=0.05,
    )

    simulator.add_sensor_config(
        sensor_type=Humidity,
        sensor_id="hum_office_01",
        min_value=40.0,
        max_value=60.0,
        jitter=0.08,
    )


if __name__ == "__main__":
    main()
