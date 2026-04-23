# LLM Protected API

Проект представляет собой защищённый backend API на FastAPI для работы с большой языковой моделью.

Реализованы:
- регистрация и аутентификация пользователей;
- JWT access и refresh токены;
- защищённые маршруты;
- интеграция с OpenRouter;
- хранение истории переписки в SQLite;
- получение и очистка истории чата.

## Стек технологий

- Python 3.11
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic
- JWT (`python-jose`)
- `passlib`
- `httpx`
- OpenRouter API
- Ruff
- uv

## Структура проекта

```text
app/
├── api/
│   ├── auth.py
│   ├── chat.py
│   └── users.py
├── models/
│   ├── chat.py
│   └── user.py
├── schemas/
│   ├── chat.py
│   └── user.py
├── services/
│   ├── chat_service.py
│   └── openrouter_service.py
├── config.py
├── database.py
├── dependencies.py
├── main.py
└── security.py
```

## Установка и запуск через uv

### 1. Клонирование проекта

bash
`git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>`
`cd llm-p`

### 2. Создание виртуального окружения

bash
`uv venv`
`source .venv/Scripts/activate`

### 3. Установка зависимостей

Если зависимости уже описаны в проекте:

bash
`uv sync`

Если нужно установить вручную:

bash
`uv add fastapi uvicorn sqlalchemy aiosqlite pydantic-settings python-jose[cryptography] passlib[bcrypt] httpx ruff email-validator "bcrypt<4"`

### 4. Настройка файла `.env`

В корне проекта необходимо создать файл `.env` и указать:

```env
APP_NAME=LLM Protected API
DATABASE_URL=sqlite+aiosqlite:///./app.db

JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-4o-mini
```

### 5. Запуск проекта

bash
`uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

### 6. Swagger UI

После запуска документация доступна по адресу:

http://127.0.0.1:8000/docs

## Реализованные эндпоинты

### Аутентификация

* `POST /auth/register` — регистрация пользователя
* `POST /auth/login` — логин и получение JWT access/refresh токенов
* `POST /auth/refresh` — обновление пары токенов

### Пользователь

* `GET /users/me` — получить информацию о текущем пользователе

### Чат

* `POST /chat` — отправка сообщения в LLM
* `GET /chat/history` — получение истории переписки
* `DELETE /chat/history` — очистка истории переписки

## Демонстрация работы

### 1. Регистрация пользователя

При регистрации использован email требуемого формата: `student_vedmalins@email.com`.

![Регистрация пользователя (request)](images\101_register.jpg)

![Регистрация пользователя (response)](images\102_register.jpg)

### 2. Логин и получение JWT токенов

![Логин и получение JWT (request)](images\201_login.jpg)

![Логин и получение JWT (response)](images\202_login.jpg)

### 3. Авторизация через Swagger

![Авторизация через Swagger](images\301_authorize.jpg)

### 4. Вызов `POST /chat`

![Вызов POST /chat-request](images\401_chat.jpg)

![Вызов POST /chat-response](images\images\402_chat.jpg)

### 5. Получение истории через `GET /chat/history`

![Получение истории чата](images\501_history.jpg)

### 6. Удаление истории через `DELETE /chat/history`

![Удаление истории чата](images\601_delete_history.jpg)

## Пример сценария работы

1. Пользователь регистрируется через `POST /auth/register`
2. Выполняет логин через `POST /auth/login`
3. Получает `access_token` и `refresh_token`
4. Авторизуется через Swagger кнопкой `Authorize`
5. Отправляет сообщение через `POST /chat`
6. Получает историю через `GET /chat/history`
7. При необходимости очищает историю через `DELETE /chat/history`

## Проверка качества кода

Проверка линтером Ruff:

`uv run ruff check .`


Результат:

`All checks passed!`

## Итог

Проект реализует защищённый API для работы с большой языковой моделью с использованием FastAPI, JWT, SQLite, SQLAlchemy и OpenRouter.
Архитектура разделена на роутеры, схемы, модели, зависимости и сервисы, что делает проект удобным для расширения.

## Архитектурные особенности

- роутеры вынесены в `app/api`
- Pydantic-схемы вынесены в `app/schemas`
- SQLAlchemy-модели вынесены в `app/models`
- логика работы с LLM вынесена в `app/services`
- зависимости авторизации вынесены в `app/dependencies`
