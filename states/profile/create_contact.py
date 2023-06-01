from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateContactState(StatesGroup):
    name = State()
    link = State()

    name_field_name = 'name'
    link_field_name = 'link'
