from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.session import get_session
from database.repositories import UserRepo, AppointmentRepo
from keyboards.booking_kb import (
    get_dates_keyboard,
    get_time_keyboard,
    get_booking_confirm_keyboard,
)
from keyboards.main_kb import get_main_keyboard
from states.forms import BookingForm
from utils.notification import notify_admin_appointment

router = Router()


@router.message(F.text == "📅 Записаться на замер")
async def start_booking(message: Message, state: FSMContext) -> None:
    async with get_session() as session:
        user_repo = UserRepo(session)
        await user_repo.get_or_create(
            message.from_user.id,
            message.from_user.username or "",
            message.from_user.first_name or "",
        )

    await state.set_state(BookingForm.date)
    await message.answer(
        "📅 <b>Выберите дату замера:</b>",
        reply_markup=get_dates_keyboard()
    )


@router.message(BookingForm.date)
async def process_date(message: Message, state: FSMContext) -> None:
    await state.update_data(date=message.text)
    await state.set_state(BookingForm.time_slot)
    await message.answer(
        "⏰ <b>Выберите удобное время:</b>",
        reply_markup=get_time_keyboard()
    )


@router.message(BookingForm.time_slot)
async def process_time_slot(message: Message, state: FSMContext) -> None:
    await state.update_data(time_slot=message.text)
    await state.set_state(BookingForm.address)
    await message.answer("📍 <b>Укажите адрес замера:</b>")


@router.message(BookingForm.address)
async def process_address(message: Message, state: FSMContext) -> None:
    await state.update_data(address=message.text)
    await state.set_state(BookingForm.phone)
    await message.answer("📱 <b>Введите ваш номер телефона:</b>")


@router.message(BookingForm.phone)
async def process_booking_phone(message: Message, state: FSMContext) -> None:
    async with get_session() as session:
        user_repo = UserRepo(session)
        await user_repo.update_phone(message.from_user.id, message.text)

    await state.update_data(phone=message.text)
    await state.set_state(BookingForm.comment)
    await message.answer("📝 <b>Комментарий к заказу (или отправьте «Пропустить»):</b>")


@router.message(BookingForm.comment)
async def process_comment(message: Message, state: FSMContext) -> None:
    comment = message.text if message.text and message.text.lower() != "пропустить" else ""
    await state.update_data(comment=comment)

    data = await state.get_data()
    resume = (
        "📋 <b>Резюме записи:</b>\n\n"
        f"📅 Дата: {data['date']}\n"
        f"⏰ Время: {data['time_slot']}\n"
        f"📍 Адрес: {data['address']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"📝 Комментарий: {data.get('comment', '—')}\n\n"
        f"Все верно?"
    )

    await state.set_state(BookingForm.confirm)
    await message.answer(resume, reply_markup=get_booking_confirm_keyboard())


@router.callback_query(BookingForm.confirm, F.data == "booking_confirm_yes")
async def confirm_booking(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()

    async with get_session() as session:
        user_repo = UserRepo(session)
        user = await user_repo.get_or_create(callback.from_user.id)

        appointment_repo = AppointmentRepo(session)
        appointment = await appointment_repo.create(user.id, data)

    bot = callback.bot
    await notify_admin_appointment(bot, data, user.id, appointment.id)

    await state.clear()
    await callback.message.answer(
        "✅ <b>Заявка на замер принята!</b>\n"
        "Менеджер свяжется с вами для подтверждения.",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()


@router.callback_query(BookingForm.confirm, F.data == "booking_confirm_edit")
async def edit_booking(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingForm.date)
    await callback.message.answer(
        "✏️ Начнём заново.\n📅 Выберите дату:",
        reply_markup=get_dates_keyboard()
    )
    await callback.answer()
