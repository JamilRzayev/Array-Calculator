import logging
from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from bot.database.repo import UserRepo, SubscriptionRepo, TransactionRepo
from bot.database.base import async_session
from bot.services.marzban import MarzbanAPI
from bot.config import config
from datetime import datetime, timedelta

router = Router()
marzban = MarzbanAPI()
logger = logging.getLogger(__name__)

TARIFFS = {
    "1_month": {"price": 300, "days": 30, "label": "1 месяц"},
    "3_month": {"price": 800, "days": 90, "label": "3 месяца"},
    "1_year": {"price": 2500, "days": 365, "label": "1 год"},
}

@router.callback_query(F.data == "deposit_stars")
async def deposit_stars(callback: types.CallbackQuery):
    # В aiogram 3.x для Stars используется send_invoice с валютой "XTR"
    # Но для этого нужно настроить цены. Оставим как пример.
    await callback.answer("Метод Telegram Stars в разработке. Используйте /add_balance для тестов.", show_alert=True)

@router.callback_query(F.data == "deposit_crypto")
async def deposit_crypto(callback: types.CallbackQuery):
    await callback.answer("Интеграция с CryptoPay в процессе. Используйте /add_balance для тестов.", show_alert=True)

@router.callback_query(F.data == "deposit_yookassa")
async def deposit_yookassa(callback: types.CallbackQuery):
    await callback.answer("Интеграция с ЮKassa в процессе. Используйте /add_balance для тестов.", show_alert=True)

@router.message(Command("add_balance"))
async def add_balance_cmd(message: types.Message):
    # Команда только для админа
    if message.from_user.id != config.ADMIN_ID:
        return

    try:
        parts = message.text.split()
        amount = float(parts[1])
        async with async_session() as session:
            user_repo = UserRepo(session)
            tx_repo = TransactionRepo(session)
            user = await user_repo.get_or_create_user(message.from_user.id)
            await user_repo.update_balance(message.from_user.id, amount)
            await tx_repo.create_transaction(user.id, amount, "deposit")
            await session.commit()

            await message.answer(f"✅ Баланс успешно пополнен на {amount} ₽")

            # Уведомление админу
            if message.from_user.id != config.ADMIN_ID:
                try:
                    await message.bot.send_message(
                        config.ADMIN_ID,
                        f"💰 Ручное пополнение баланса!\n"
                        f"Пользователь: @{message.from_user.username} ({message.from_user.id})\n"
                        f"Сумма: {amount} ₽"
                    )
                except Exception as e:
                    logger.error(f"Failed to notify admin: {e}")

    except (IndexError, ValueError):
        await message.answer("Использование: /add_balance <сумма>")

@router.callback_query(F.data.startswith("buy_"))
async def process_buy_subscription(callback: types.CallbackQuery, bot: Bot):
    tariff_key = callback.data.replace("buy_", "")
    if tariff_key not in TARIFFS:
        return

    tariff = TARIFFS[tariff_key]
    async with async_session() as session:
        user_repo = UserRepo(session)
        sub_repo = SubscriptionRepo(session)
        tx_repo = TransactionRepo(session)

        user = await user_repo.get_or_create_user(callback.from_user.id)

        if user.balance < tariff["price"]:
            await callback.answer("❌ Недостаточно средств на балансе. Пополните баланс.", show_alert=True)
            return

        # Работа с Marzban
        marzban_username = f"user_{user.telegram_id}"
        expiry_date = datetime.utcnow() + timedelta(days=tariff["days"])
        expire_timestamp = int(expiry_date.timestamp())

        # Проверяем, есть ли уже пользователь в Marzban
        marzban_user = await marzban.get_user(marzban_username)

        success = False
        if marzban_user:
            # Продлеваем
            current_expire = marzban_user.get("expire")
            if current_expire and current_expire > int(datetime.utcnow().timestamp()):
                expiry_date = datetime.fromtimestamp(current_expire) + timedelta(days=tariff["days"])
                expire_timestamp = int(expiry_date.timestamp())

            if await marzban.update_user(marzban_username, expire=expire_timestamp):
                success = True
        else:
            # Создаем нового
            if await marzban.create_user(marzban_username, expire=expire_timestamp):
                success = True

        if not success:
            error_msg = "❌ Ошибка при взаимодействии с VPN-сервером. Попробуйте позже."
            # Если это админ, дадим больше инфы
            if callback.from_user.id == config.ADMIN_ID:
                error_msg += "\n\n⚠️ Админ-подсказка: Проверьте логи бота и доступность Marzban API. Используйте /test_marzban"
            await callback.answer(error_msg, show_alert=True)
            return

        # Списание средств, создание подписки и транзакции в одной БД-транзакции
        try:
            await user_repo.update_balance(user.telegram_id, -tariff["price"])
            await sub_repo.create_subscription(user.id, marzban_username, expiry_date)
            await tx_repo.create_transaction(user.id, -tariff["price"], "purchase")
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database error during purchase: {e}")
            await callback.answer("❌ Ошибка при сохранении данных. Обратитесь в поддержку.", show_alert=True)
            return

        await callback.message.edit_text(
            f"✅ Подписка успешно оформлена/продлена!\n"
            f"Тариф: {tariff['label']}\n"
            f"Действует до: {expiry_date.strftime('%d.%m.%Y')}\n\n"
            f"🔗 Ваша ссылка: <code>{marzban.get_subscription_link(marzban_username)}</code>",
            parse_mode="HTML"
        )

        # Уведомление админу
        try:
            await bot.send_message(
                config.ADMIN_ID,
                f"🛍 Новая покупка!\n"
                f"Пользователь: @{callback.from_user.username} ({callback.from_user.id})\n"
                f"Тариф: {tariff['label']}\n"
                f"Сумма: {tariff['price']} ₽"
            )
        except Exception as e:
            logger.error(f"Failed to notify admin: {e}")

    await callback.answer()
