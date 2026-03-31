from aiogram.fsm.state import State, StatesGroup

class QuizFrom(StatesGroup):
    furniture_type = State()
    sizes = State()
    budget = State()
    location = State()
    phone = State()
    description = State()
    confirm = State()


class BookingForm(StatesGroup):
    pass
