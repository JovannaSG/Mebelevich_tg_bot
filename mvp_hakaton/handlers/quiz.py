from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.fake_db import (
    get_or_create_user,
    update_user_phone,
    create_lead
)
from keyboards.quiz_kb import (
    get_furniture_type_keyboard,
    get_budget_keyboard,
    get_confirm_keyboard
)
from states.forms import QuizForm

router = Router()


@router.message(F.text == "🛋 Рассчитать мебель")
async def start_quiz(message: Message, state: FSMContext) -> None:
    get_or_create_user(
        message.from_user.id,
        message.from_user.username or "",
        message.from_user.first_name or ""
    )
    await state.set_state(QuizForm.furniture_type)
    await message.answer(
        "🛋 <b>Какой тип мебели вас интересует?</b>",
        reply_markup=get_furniture_type_keyboard()
    )


@router.message(QuizForm.furniture_type)
async def process_furniture_type(message: Message, state: FSMContext) -> None:
    await state.update_data(furniture_type=message.text)
    await state.set_state(QuizForm.sizes)
    await message.answer("📏 <b>Укажите размеры (ШхВхГ в см):</b>")


@router.message(QuizForm.sizes)
async def process_sizes(message: Message, state: FSMContext):
    await state.update_data(sizes=message.text)
    await state.set_state(QuizForm.budget)
    await message.answer(
        "💰 <b>Какой у вас бюджет?</b>",
        reply_markup=get_budget_keyboard()
    )


@router.message(QuizForm.budget)
async def process_budget(message: Message, state: FSMContext) -> None:
    await state.update_data(budget=message.text)
    await state.set_state(QuizForm.location)
    await message.answer("📍 <b>Укажите город и район:</b>")


@router.message(QuizForm.location)
async def process_location(message: Message, state: FSMContext) -> None:
    await state.update_data(location=message.text)
    await state.set_state(QuizForm.phone)
    await message.answer("📱 <b>Введите ваш номер телефона:</b>")


@router.message(QuizForm.phone)
async def process_phone(message: Message, state: FSMContext) -> None:
    update_user_phone(message.from_user.id, message.text)
    await state.update_data(phone=message.text)
    await state.set_state(QuizForm.description)
    await message.answer("📝 <b>Опишите проект (или «Пропустить»):</b>")


@router.message(QuizForm.description)
async def process_description(message: Message, state: FSMContext) -> None:
    if message.text.lower():
        desc = ""
    else:
        message.text
    await state.update_data(description=desc)
    
    data = await state.get_data()
    resume = (
        "📋 <b>Резюме заявки:</b>\n\n"
        f"🛋 Тип: {data['furniture_type']}\n"
        f"📏 Размеры: {data['sizes']}\n"
        f"💰 Бюджет: {data['budget']}\n"
        f"📍 Локация: {data['location']}\n"
        f"📱 Телефон: {data['phone']}\n\n"
        f"Все верно?"
    )
    
    await state.set_state(QuizForm.confirm)
    await message.answer(resume, reply_markup=get_confirm_keyboard())


@router.callback_query(QuizForm.confirm, F.data == "confirm_yes")
async def confirm_lead(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    user = get_or_create_user(callback.from_user.id)
    lead = create_lead(user["id"], data)
    
    await state.clear()
    await callback.message.answer("✅ <b>Заявка принята!</b>")


@router.callback_query(QuizForm.confirm, F.data == "confirm_edit")
async def edit_lead(callback: CallbackQuery, state: FSMContext):
    await state.set_state(QuizForm.furniture_type)
    await callback.message.answer(
        "✏️ Начнём заново.\n🛋 Тип мебели?",
        reply_markup=get_furniture_type_keyboard()
    )
