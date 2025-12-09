# GraduateWork - Система мониторинга датчиков с предиктивной аналитикой

Проект реализует полную систему сбора, анализа и предсказания данных с датчиков с автоматической отправкой уведомлений о критических ситуациях.

## Архитектура системы

- **Collector** - собирает данные с датчиков через имитационные устройства
- **Sensors** - модуль с классами сенсоров различных типов
- **Core** - API-шлюз на FastAPI для взаимодействия компонентов и хранения данных
- **Predictor** - сервис машинного обучения для онлайн-предсказаний
- **Alarm** - модули отправки уведомлений (console, telegram и др.)

## Быстрый запуск

### Запуск полной системы через Docker Compose

1. Клонируйте репозиторий:
```bash
git clone <repository_url>
cd GraduateWork
```

2. Создайте файл окружения на основе примера:
```bash
cp .env.example .env
```

3. Запустите все сервисы:
```bash
docker-compose up --build
```

Это запустит следующие сервисы:
- **Collector** (порт: автоматически определяется Docker)
- **Core API** (порт: 8000)
- **Database** (PostgreSQL, порт: 5432)
- **Cache** (Redis, порт: 6379)
- **Predictor** (порт: автоматически определяется Docker)

### Запуск отдельных компонентов

#### Core API
```bash
cd core
pip install -r requirements.txt
python run.py
```

#### Collector
```bash
# Установите зависимости для коллектора
cd collector
pip install -r requirements.txt

# Запустите симулятор данных
python src/collector/main.py
```

#### Predictor
```bash
cd predictor
pip install -r requirements.txt
python main.py
```

#### Alarm сервисы
Console:
```bash
cd alarm/console
pip install -r requirements.txt
python main.py
```

Telegram:
```bash
cd alarm/telegram
pip install -r requirements.txt
python main.py
```

## Функциональность

- Сбор данных с имитаторов датчиков
- Хранение данных в PostgreSQL
- Онлайн-обучение моделей предсказания для каждого датчика
- Предсказание значений датчиков на несколько шагов вперед
- Автоматическая отправка алертов при обнаружении опасных ситуаций
- Отправка уведомлений через WebSocket различным Alarm-сервисам

## API документация

После запуска Core API доступно по адресу: http://localhost:8000

Документация автоматически генерируется и доступна по:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Текущий статус

Проект находится на этапе разработки. Описание архитектуры и плана реализации доступно в [TODO.md](./TODO.md).