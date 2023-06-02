from aiogram.dispatcher.filters.state import State, StatesGroup


class AddSkillsState(StatesGroup):
    skills = State()
