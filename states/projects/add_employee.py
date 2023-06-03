from aiogram.dispatcher.filters.state import State, StatesGroup


class AddEmployeeState(StatesGroup):
    user_id = State()
