from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard: list[list[KeyboardButton]] = [
        [KeyboardButton(text="🛋 Рассчитать мебель")],
        [KeyboardButton(text="📅 Записаться на замер")],
        [KeyboardButton(text="💬 Связаться с менеджером")]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
