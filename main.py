import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from bot.config import config
from bot.handlers import user, payments, admin
from bot.database.base import init_db

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Инициализация БД
    await init_db()

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(admin.router)
    dp.include_router(user.router)
    dp.include_router(payments.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
