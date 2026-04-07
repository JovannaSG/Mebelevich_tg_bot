from aiogram import Bot

from config import settings


async def notify_admin_lead(bot: Bot, data: dict, lead_id: int) -> None:
    text = (
        "🔥 <b>Новый лид!</b>\n\n"
        f"🆔 #{lead_id}\n"
        f"🛋 {data.get('furniture_type')}\n"
        f"📏 {data.get('sizes')}\n"
        f"💰 {data.get('budget')}\n"
        f"📍 {data.get('location')}\n"
        f"📱 {data.get('phone')}\n"
    )
    for admin_id in settings.bot_admin_ids:
        try:
            await bot.send_message(admin_id, text)
        except Exception:
            pass
