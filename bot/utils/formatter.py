def format_profile(full_name: str, telegram_id: int, balance: float, subscription_info: str):
    return (
        f"👤 <b>Профиль</b>\n"
        f"• Имя: {full_name}\n"
        f"• ID: <code>{telegram_id}</code>\n"
        f"• Баланс: {balance:.2f} ₽\n\n"
        f"🔑 <b>Ваша подписка:</b> {subscription_info}\n"
        f"💳 Нажмите 'Купить подписку' чтобы начать пользоваться VPN\n\n"
        f"💡 Используйте кнопки ниже для управления подпиской"
    )
