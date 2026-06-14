from aiogram import Router, types, F
from aiogram.filters import Command
from bot.config import config
from bot.services.marzban import MarzbanAPI
import logging

router = Router()
marzban = MarzbanAPI()
logger = logging.getLogger(__name__)

@router.message(Command("test_marzban"))
async def test_marzban_cmd(message: types.Message):
    if message.from_user.id != config.ADMIN_ID:
        return

    await message.answer(f"🔍 Тестирую подключение к Marzban...\nАдрес: {config.MARZBAN_ADDRESS}")

    import socket
    from urllib.parse import urlparse

    try:
        parsed_url = urlparse(config.MARZBAN_ADDRESS)
        hostname = parsed_url.hostname
        if hostname:
            ip = socket.gethostbyname(hostname)
            await message.answer(f"🌐 Хост {hostname} разрешен в IP: {ip}")
    except Exception as e:
        await message.answer(f"❌ Ошибка разрешения DNS: {e}")

    # Проверка общей связности
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://google.com", timeout=5.0)
            await message.answer(f"✅ Интернет доступен (Google: {resp.status_code})")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка доступа в интернет: {e}. Возможно, контейнер изолирован.")

    if "localhost" in config.MARZBAN_ADDRESS or "127.0.0.1" in config.MARZBAN_ADDRESS:
        await message.answer("⚠️ Внимание: Вы используете 'localhost'. Внутри Docker это означает 'внутри контейнера'. "
                             "Если Marzban запущен на том же ПК, используйте 'http://host.docker.internal:8000'")

    token = await marzban._get_token()
    if not token:
        await message.answer("❌ Ошибка: Не удалось получить токен. Проверьте адрес, логин/пароль и доступность сервера в логах бота.")
        return

    await message.answer("✅ Токен успешно получен!")

    # Попробуем получить инфо о самой панели (обычно это GET /api/system)
    # Но в нашем MarzbanAPI этого нет, просто проверим get_user для несуществующего юзера
    user = await marzban.get_user("non_existent_user_12345")
    # Если мы здесь, значит запрос прошел (даже если 404)
    await message.answer("✅ Соединение с API установлено!")
