from aiogram.dispatcher.filters.state import State, StatesGroup


class ExperienceRetrieveState(StatesGroup):
    value = State()
