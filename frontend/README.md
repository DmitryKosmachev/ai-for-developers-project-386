# Фронтенд «Запись на созвон»

UI приложения. Отдельная часть, работает с бэкендом **только** через API-контракт
(`../spec/dist/openapi.yaml`). Во время разработки бэкенд заменяется mock-сервером Prism.

## Стек

React 18 + Vite + TypeScript · Tailwind CSS v4 + shadcn/ui · React Router ·
TanStack Query · openapi-fetch (+ типы из контракта) · lucide-react · sonner.

## Быстрый старт

```bash
npm install

# 1) В одном терминале — mock API из контракта (порт 4010)
npm run mock

# 2) В другом — dev-сервер UI (порт 5173)
npm run dev
```

Откройте http://localhost:5173.

Чтобы подключить реальный бэкенд вместо Prism, задайте адрес в `.env`:

```
VITE_API_BASE_URL=http://localhost:3000
```

(см. `.env.example`).

## Скрипты

| Скрипт | Назначение |
|---|---|
| `npm run dev` | Dev-сервер Vite |
| `npm run build` | Проверка типов + production-сборка в `dist/` |
| `npm run mock` | Prism mock-сервер из `../spec/dist/openapi.yaml` |
| `npm run gen:api` | Перегенерировать типы (`src/api/schema.d.ts`) из контракта |
| `npm run lint` | ESLint |

## Структура

```
src/
  api/            # клиент, хуки TanStack Query, типы из контракта
  components/
    ui/           # shadcn-примитивы (button, card, input, ...)
    layout/       # шапка, layout гостя и админки
    theme-provider, mode-toggle, states
  lib/            # cn(), форматирование дат/слотов
  pages/
    HomePage          # гость: профиль владельца + список типов встреч
    BookingPage       # гость: выбор слота + форма + подтверждение
    admin/            # владелец: список встреч, создание типов событий
```

## Страницы

- `/` — список видов брони (гость).
- `/book/:eventTypeId` — выбор слота из 14-дневного окна и запись.
- `/admin` — предстоящие встречи (владелец).
- `/admin/event-types` — создание типов событий.

## Темы

Переключатель в шапке: **светлая / тёмная / системная** (по умолчанию — системная,
выбор сохраняется в localStorage).

## Контракт — источник правды

При изменении контракта: пересоберите OpenAPI в `../spec`, затем `npm run gen:api`
здесь и поправьте затронутые места (TypeScript подсветит несоответствия).
