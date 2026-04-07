from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from keyboards.main_kb import get_main_keyboard
from database.repositories import UserRepository

router = Router(name="main commands")


@router.message(Command("start"))
async def start_cmd(message: Message) -> None:
    await UserRepository.get_or_create(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "",
        first_name=message.from_user.first_name or ""
    )

    await message.answer(
        f"👋 Здравствуйте, {message.from_user.first_name}!\n\n"
        f"Добро пожаловать в бот «Мебелевич»!\n"
        f"Выберите действие:",
        reply_markup=get_main_keyboard()
    )


@router.message(F.text == "💬 Связаться с менеджером")
async def contact_manager(message: Message) -> None:
    await message.answer(
        "📞 Для связи с менеджером:\n"
        "Телефон: +7 (XXX) XXX-XX-XX\n"
        "Telegram: @mebelevich_manager"
    )
