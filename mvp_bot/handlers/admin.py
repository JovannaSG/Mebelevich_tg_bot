from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from database.session import get_session
from database.repositories import UserRepo, LeadRepo, AppointmentRepo
from config import settings

router = Router()


def is_admin(user_id: int) -> bool:
    return str(user_id) in settings.bot_admin_ids


@router.message(Command("leads"))
async def cmd_leads(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return

    async with get_session() as session:
        lead_repo = LeadRepo(session)
        leads = await lead_repo.get_all(limit=10)

    if not leads:
        await message.answer("📋 Нет лидов.")
        return

    lines = ["📋 <b>Последние лиды:</b>\n"]
    for lead in leads:
        lines.append(
            f"#{lead.id} | {lead.furniture_type} | {lead.budget} | {lead.created_at.strftime('%d.%m.%Y')}"
        )

    await message.answer("\n".join(lines))


@router.message(Command("appointments"))
async def cmd_appointments(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return

    async with get_session() as session:
        appointment_repo = AppointmentRepo(session)
        appointments = await appointment_repo.get_all(limit=10)

    if not appointments:
        await message.answer("📅 Нет записей на замер.")
        return

    lines = ["📅 <b>Последние записи:</b>\n"]
    for a in appointments:
        lines.append(
            f"#{a.id} | {a.appointment_date} {a.time_slot} | {a.address}"
        )

    await message.answer("\n".join(lines))


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return

    async with get_session() as session:
        user_repo = UserRepo(session)
        lead_repo = LeadRepo(session)
        appointment_repo = AppointmentRepo(session)

        users_count = await user_repo.count()
        leads_count = await lead_repo.count()
        new_leads = await lead_repo.count_new()
        appointments_count = await appointment_repo.count()

    text = (
        "📊 <b>Статистика</b>\n\n"
        f"👤 Пользователей: {users_count}\n"
        f"📋 Лидов всего: {leads_count}\n"
        f"🔥 Новых лидов: {new_leads}\n"
        f"📅 Записей на замер: {appointments_count}"
    )

    await message.answer(text)
