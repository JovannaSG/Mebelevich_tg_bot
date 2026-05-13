from aiogram.fsm.state import State, StatesGroup


class QuizForm(StatesGroup):
    furniture_type = State()
    sizes = State()
    budget = State()
    location = State()
    phone = State()
    description = State()
    confirm = State()


class BookingForm(StatesGroup):
    date = State()
    time_slot = State()
    address = State()
    phone = State()
    comment = State()
    confirm = State()
