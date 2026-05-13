from datetime import datetime, timedelta

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)


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


def get_booking_confirm_keyboard() -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="booking_confirm_yes")],
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="booking_confirm_edit")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
