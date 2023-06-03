from aiogram.dispatcher.filters.state import State, StatesGroup


class UpdateRoleState(StatesGroup):
    role = State()
