from datetime import datetime, timedelta

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)


def get_furniture_type_keyboard() -> ReplyKeyboardMarkup:
    types: list[str] = [
        "Кухня", "Шкаф",
        "Гардеробная", "Детская",
        "Гостиная", "Другое"
    ]
    keyboard: list[list[KeyboardButton]] = [
        [KeyboardButton(text=t)] for t in types
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_budget_keyboard() -> ReplyKeyboardMarkup:
    budgets: list[str] = [
        "До 50 000 ₽",
        "50 000 - 100 000 ₽",
        "100 000 - 200 000 ₽",
        "Более 200 000 ₽"
    ]
    keyboard: list[list[KeyboardButton]] = [
        [KeyboardButton(text=b)] for b in budgets
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_confirm_keyboard() -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_yes")],
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="confirm_edit")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_dates_keyboard() -> ReplyKeyboardMarkup:
    dates: list[str] = []
    for i in range(7):
        date = datetime.now() + timedelta(days=i)
        dates.append(date.strftime("%d.%m.%Y"))

    keyboard: list[list[KeyboardButton]] = [
        [KeyboardButton(text=d)] for d in dates
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_time_keyboard() -> ReplyKeyboardMarkup:
    times: list[str] = [
        "10:00-12:00",
        "12:00-14:00",
        "14:00-16:00",
        "16:00-18:00",
        "18:00-20:00"
    ]
    keyboard: list[list[KeyboardButton]] = [
        [KeyboardButton(text=t)] for t in times
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
