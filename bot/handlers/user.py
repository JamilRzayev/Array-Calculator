from aiogram import Router, types, F
from aiogram.filters import CommandStart
from bot.keyboards.main_menu import get_main_menu, get_balance_menu, get_tariffs_menu, get_deposit_methods
from bot.database.repo import UserRepo, SubscriptionRepo
from bot.database.base import async_session
from bot.services.marzban import MarzbanAPI
from bot.utils.formatter import format_profile
from datetime import datetime

router = Router()
marzban = MarzbanAPI()

async def show_profile(message_or_callback, user_obj: types.User):
    async with async_session() as session:
        user_repo = UserRepo(session)
        sub_repo = SubscriptionRepo(session)
        user = await user_repo.get_or_create_user(user_obj.id, user_obj.username)

        subs = await sub_repo.get_user_subscriptions(user.id)

        status_text = "не активна"
        if subs:
            # Берем самую свежую подписку
            sub = subs[-1]
            if sub.expiry_date > datetime.utcnow():
                status_text = f"активна до {sub.expiry_date.strftime('%d.%m.%Y')}\n🔗 Ссылка: <code>{marzban.get_subscription_link(sub.marzban_username)}</code>"
            else:
                status_text = f"истекла {sub.expiry_date.strftime('%d.%m.%Y')}"

        text = format_profile(
            user_obj.full_name,
            user_obj.id,
            user.balance,
            status_text
        )

        if isinstance(message_or_callback, types.Message):
            await message_or_callback.answer(text, reply_markup=get_main_menu(), parse_mode="HTML")
        else:
            await message_or_callback.message.edit_text(text, reply_markup=get_main_menu(), parse_mode="HTML")

@router.message(CommandStart())
async def start_command(message: types.Message):
    await show_profile(message, message.from_user)

@router.callback_query(F.data == "start")
async def back_to_start(callback: types.CallbackQuery):
    await show_profile(callback, callback.from_user)
    await callback.answer()

@router.callback_query(F.data == "balance")
async def balance_menu(callback: types.CallbackQuery):
    async with async_session() as session:
        user_repo = UserRepo(session)
        user = await user_repo.get_or_create_user(callback.from_user.id)
        await callback.message.edit_text(
            f"💰 Ваш баланс: {user.balance:.2f} ₽",
            reply_markup=get_balance_menu()
        )
    await callback.answer()

@router.callback_query(F.data == "deposit")
async def deposit_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите способ пополнения:", reply_markup=get_deposit_methods())
    await callback.answer()

@router.callback_query(F.data == "buy_subscription")
async def buy_subscription_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите тарифный план:", reply_markup=get_tariffs_menu())
    await callback.answer()

@router.callback_query(F.data == "help")
async def help_handler(callback: types.CallbackQuery):
    # Как просил юзер - перекидывает на юзера (админа)
    await callback.message.answer("По всем вопросам обращайтесь к администратору: @vpn_support_bot_admin")
    await callback.answer()

@router.callback_query(F.data.in_(["trial", "gift", "referral", "proxy"]))
async def placeholders_handler(callback: types.CallbackQuery):
    await callback.answer("Данный раздел пока находится в разработке.", show_alert=True)
