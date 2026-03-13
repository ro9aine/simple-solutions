# Deribit Price Service

Сервис собирает `index price` для `BTC_USD` и `ETH_USD` с биржи Deribit раз в минуту, сохраняет значения в PostgreSQL и отдает данные через внешнее API на FastAPI.

## Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Celery + Celery Beat
- Redis
- aiohttp
- pytest
- Docker Compose

## Project structure

```text
app/
  api/          # FastAPI routes and dependencies
  clients/      # Deribit HTTP client
  core/         # Settings
  db/           # Engine and session factory
  models/       # SQLAlchemy models
  repositories/ # Data access layer
  schemas/      # Pydantic DTOs
  services/     # Business logic
  tasks/        # Celery app and scheduled jobs
tests/
```

## API

Все методы используют `GET` и требуют query-параметр `ticker`.

### 1. Получить все сохраненные данные по тикеру

```http
GET /prices?ticker=BTC_USD
```

### 2. Получить последнюю цену по тикеру

```http
GET /prices/latest?ticker=BTC_USD
```

### 3. Получить цены по диапазону дат

```http
GET /prices/by-date?ticker=BTC_USD&start_timestamp=1700000000&end_timestamp=1700003600
```

`start_timestamp` и `end_timestamp` передаются в UNIX timestamp. Нужно указать хотя бы один из параметров.

## Local run

1. Установить Python 3.11 и PostgreSQL/Redis либо использовать Docker Compose.
2. Скопировать `.env.example` в `.env` и при необходимости изменить значения.
3. Установить зависимости:

```bash
pip install -e .[dev]
```

4. Запустить API:

```bash
uvicorn app.main:app --reload
```

5. Запустить Celery worker:

```bash
celery -A app.tasks.celery_app:celery_app worker --loglevel=info
```

6. Запустить Celery Beat:

```bash
celery -A app.tasks.celery_app:celery_app beat --loglevel=info
```

## Docker

Запуск всего окружения:

```bash
docker compose up --build
```

Сервисы:

- `api` на `http://localhost:8000`
- `db` на `localhost:5432`
- `worker` выполняет Celery tasks
- `beat` запускает планировщик раз в минуту
- `redis` используется как Celery broker/result backend

## Tests

```bash
pytest
```

## Design decisions

- Выделены слои `repository` и `service`, чтобы HTTP-слой не зависел напрямую от SQLAlchemy.
- В таблице хранится UNIX timestamp, потому что это прямо требуется в задании и упрощает фильтрацию.
- Для клиента Deribit использован `aiohttp`, так как это указано в необязательных требованиях и хорошо подходит для внешних HTTP-вызовов.
- Celery Beat запускает задачу раз в минуту, а worker выполняет сохранение в БД. Такой вариант отделяет API от фоновой синхронизации.
- Для простоты тестового проекта миграции не добавлялись: схема создается через `create_all()` при старте приложения и worker. Для production-проекта стоило бы подключить Alembic.

## Notes

- Используется публичный endpoint Deribit `public/get_index_price`.
- В Swagger документация доступна по адресу `/docs`.
