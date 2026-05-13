from aiogram import Bot

from config import ADMIN_IDS


async def notify_admin_lead(
    bot: Bot,
    data: dict,
    user_id: int,
    lead_id: int
) -> None:
    text = (
        "🔥 <b>Новый лид!</b>\n\n"
        f"🆔 #{lead_id}\n"
        f"🛋 {data.get('furniture_type')}\n"
        f"📏 {data.get('sizes')}\n"
        f"💰 {data.get('budget')}\n"
        f"📍 {data.get('location')}\n"
        f"📱 {data.get('phone')}\n"
    )
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text)
        except:
            pass


async def notify_admin_appointment(
    bot: Bot, 
    dict,
    user_id: int,
    appointment_id: int
) -> None:
    text = (
        "📅 <b>Новая запись!</b>\n\n"
        f"🆔 #{appointment_id}\n"
        f"📅 {data.get('date')} {data.get('time_slot')}\n"
        f"📍 {data.get('address')}\n"
        f"📱 {data.get('phone')}\n"
    )
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text)
        except:
            pass