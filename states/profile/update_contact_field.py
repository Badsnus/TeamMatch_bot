from aiogram.dispatcher.filters.state import State, StatesGroup


class UpdateContactFieldState(StatesGroup):
    value = State()
