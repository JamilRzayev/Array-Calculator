from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🛒 Купить подписку", callback_data="buy_subscription"))
    builder.row(types.InlineKeyboardButton(text="🎁 Пробный период", callback_data="trial"))
    builder.row(types.InlineKeyboardButton(text="💰 Баланс", callback_data="balance"))
    builder.row(types.InlineKeyboardButton(text="🤝 Подарить", callback_data="gift"))
    builder.row(types.InlineKeyboardButton(text="👥 Партнерская программа", callback_data="referral"))
    builder.row(types.InlineKeyboardButton(text="💡 Помощь", callback_data="help"))
    builder.row(types.InlineKeyboardButton(text="🛰 Прокси для Телеграмм", callback_data="proxy"))
    return builder.as_markup()

def get_balance_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="deposit"))
    builder.row(types.InlineKeyboardButton(text="🔙 Назад", callback_data="start"))
    return builder.as_markup()

def get_deposit_methods():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="⭐ Telegram Stars", callback_data="deposit_stars"))
    builder.row(types.InlineKeyboardButton(text="🪙 CryptoBot", callback_data="deposit_crypto"))
    builder.row(types.InlineKeyboardButton(text="💳 ЮKassa", callback_data="deposit_yookassa"))
    builder.row(types.InlineKeyboardButton(text="🔙 Назад", callback_data="balance"))
    return builder.as_markup()

def get_tariffs_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="1 месяц — 300 руб", callback_data="buy_1_month"))
    builder.row(types.InlineKeyboardButton(text="3 месяца — 800 руб", callback_data="buy_3_month"))
    builder.row(types.InlineKeyboardButton(text="1 год — 2500 руб", callback_data="buy_1_year"))
    builder.row(types.InlineKeyboardButton(text="🔙 Назад", callback_data="start"))
    return builder.as_markup()
