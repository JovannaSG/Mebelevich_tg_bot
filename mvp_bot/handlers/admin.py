from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config import settings
from database.repositories import LeadRepository, StatsRepository

router = Router(name="admin commands")


def is_admin(user_id: int) -> bool:
    return str(user_id) in settings.bot_admin_ids


@router.message(Command("admin"))
async def admin_panel(message: Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("⛔ У вас нет доступа к админ-панели.")
        return

    stats = await StatsRepository.get_stats()
    text = (
        "📊 <b>Админ-панель</b>\n\n"
        f"👥 Пользователей: {stats['users_count']}\n"
        f"📝 Всего заявок: {stats['leads_count']}\n"
        f"🆕 Новых заявок: {stats['new_leads']}\n\n"
        "<b>Команды:</b>\n"
        "/stats - Статистика\n"
        "/leads - Список заявок"
    )
    await message.answer(text)


@router.message(Command("stats"))
async def show_stats(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return

    stats = await StatsRepository.get_stats()
    text = (
        "📊 <b>Статистика</b>\n\n"
        f"👥 Пользователей: {stats['users_count']}\n"
        f"📝 Всего заявок: {stats['leads_count']}\n"
        f"🆕 Новых заявок: {stats['new_leads']}"
    )
    await message.answer(text)


@router.message(Command("leads"))
async def show_leads(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return

    leads = await LeadRepository.get_all(limit=10)
    
    if not leads:
        await message.answer("📭 Заявок пока нет.")
        return

    text_parts = ["📝 <b>Последние заявки:</b>\n"]
    
    for i, lead in enumerate(leads, 1):
        text_parts.append(
            f"\n{i}. #{lead.id} | {lead.furniture_type}\n"
            f"   💰 {lead.budget} | 📍 {lead.location}\n"
            f"   📱 {lead.phone} | {lead.created_at.strftime('%d.%m %H:%M')}"
        )
    
    await message.answer("\n".join(text_parts))
