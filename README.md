# Telegram VPN Bot (Marzban Integration)

Бот для продажи VPN подписок (VLESS+Reality) через панель Marzban.

## Стек технологий
- **Python 3.11+**
- **aiogram 3.x** (Telegram Bot API)
- **PostgreSQL** + **SQLAlchemy 2.0** (Database)
- **Marzban API** (VPN Management)
- **Docker** & **Docker Compose**

## Установка и запуск

1. **Клонируйте репозиторий.**
2. **Настройте переменные окружения:**
   Скопируйте `.env.example` в `.env` и заполните данные:
   ```bash
   cp .env.example .env
   ```
   Вам понадобятся:
   - `BOT_TOKEN` от @BotFather
   - `ADMIN_ID` (ваш ID в Telegram)
   - Данные для подключения к Marzban API

3. **Запустите проект через Docker Compose:**
   ```bash
   docker-compose up -d --build
   ```

### Решение проблем с подключением (Troubleshooting)
Если бот не может соединиться с Marzban (`ConnectError`):
- **DNS:** Убедитесь, что домен Marzban резолвится внутри контейнера (используйте `/test_marzban`).
- **Локальный Marzban:** Если Marzban запущен на той же машине, что и Docker (Windows/Mac), используйте `http://host.docker.internal:8000`.
- **Docker Network:** Проверьте, что контейнер имеет доступ в интернет.
- **SSL:** Если используете самоподписанный сертификат, установите `MARZBAN_SKIP_SSL_VERIFY=True`.

## Команды для тестов
- `/start` — Открыть профиль и главное меню.
- `/add_balance <сумма>` — Пополнить баланс (команда для тестирования).

## Структура проекта
- `bot/handlers/` — Обработка сообщений и нажатий кнопок.
- `bot/services/` — Клиент для взаимодействия с Marzban API.
- `bot/database/` — Модели данных и репозитории для PostgreSQL.
- `bot/keyboards/` — Инлайн-клавиатуры.
