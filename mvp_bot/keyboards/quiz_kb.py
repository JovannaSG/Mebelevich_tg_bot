from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_furniture_type_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="🛏 Шкаф", callback_data="furniture_шкаф"),
            InlineKeyboardButton(text="🛋 Диван", callback_data="furniture_диван"),
        ],
        [
            InlineKeyboardButton(text="🪑 Кухня", callback_data="furniture_кухня"),
            InlineKeyboardButton(text="🪑 Стол", callback_data="furniture_стол"),
        ],
        [
            InlineKeyboardButton(text="🛏 Кровать", callback_data="furniture_кровать"),
            InlineKeyboardButton(text="🪑 Другое", callback_data="furniture_другое"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_budget_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="💰 до 50 000", callback_data="budget_до_50000"),
            InlineKeyboardButton(text="💰 50 000-100 000", callback_data="budget_50000_100000"),
        ],
        [
            InlineKeyboardButton(text="💰 100 000-200 000", callback_data="budget_100000_200000"),
            InlineKeyboardButton(text="💰 более 200 000", callback_data="budget_200000+"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_confirm_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Да, всё верно", callback_data="confirm_yes"),
        ],
        [
            InlineKeyboardButton(text="✏️ Перезаполнить", callback_data="confirm_edit"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
