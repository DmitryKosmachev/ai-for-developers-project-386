# Бэкенд «Запись на созвон»

Серверная часть — реализация API по контракту (`../spec/dist/openapi.yaml`).
Отдельный API для фронтенд-клиента. Бизнес-правила бронирования — на сервере.
Хранилище **в памяти**: данные сбрасываются при перезапуске.

## Стек

Python 3.12 · FastAPI · Uvicorn · Pydantic v2 · pytest.

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt   # или requirements.txt без тестовых пакетов

# dev-сервер с автоперезагрузкой на http://localhost:8000
uvicorn app.main:app --reload --port 8000
```

Документация OpenAPI (Swagger UI) доступна на `http://localhost:8000/docs`.

## Тесты

```bash
pytest
```

28 тестов: генерация слотов, валидация времени, все эндпоинты, сценарии
бронирования (201 / 409 / 422 / 404). Написаны по TDD.

## Подключение фронтенда

Фронтенд ходит на адрес из `VITE_API_BASE_URL`. Чтобы он работал с этим бэкендом:

```bash
cd ../frontend
VITE_API_BASE_URL=http://localhost:8000 npm run dev
```

CORS открыт для всех источников (dev).

## Структура

```
app/
  main.py          # FastAPI, CORS, обработчики ошибок -> { code, message }
  config.py        # константы: слот 30 мин, окно 14 дней, пн–пт 09:00–18:00, tz
  models.py        # Pydantic-схемы (camelCase наружу, как в контракте)
  store.py         # in-memory хранилище + сид (владелец + 3 типа событий)
  scheduling.py    # ядро: генерация слотов, is_valid_start, пересечение интервалов
  routers/         # owner, event_types, bookings
tests/             # pytest
```

## Бизнес-правила

- Слоты — 30-минутная сетка, пн–пт 09:00–18:00 (по `Europe/Moscow`), окно 14 дней.
- Событие длительностью N минут занимает интервал N минут; слот доступен, если не в
  прошлом, помещается до 18:00 и не пересекается ни с одной бронью (глобально, для
  всех типов событий).
- Повторная запись на пересекающееся время → `409 slot_taken`.
- `Booking.end` и идентификаторы вычисляет сервер.

## API

| Метод | Путь | Назначение |
|---|---|---|
| GET | /owner | Профиль владельца |
| GET | /event-types | Список типов событий |
| GET | /event-types/{id} | Тип события (404, если нет) |
| GET | /event-types/{id}/slots | Свободные слоты на 14 дней |
| POST | /event-types | Создать тип события (422 при durationMinutes не кратном 30) |
| POST | /bookings | Создать бронь (404 / 409 / 422) |
| GET | /bookings | Все предстоящие встречи (сортировка по start) |
