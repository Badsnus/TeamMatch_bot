from aiogram.dispatcher.filters.state import State, StatesGroup


class EditNameState(StatesGroup):
    name = State()
