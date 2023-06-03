from aiogram.dispatcher.filters.state import State, StatesGroup


class UpdateCandidateDataState(StatesGroup):
    value = State()
