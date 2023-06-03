from enum import Enum

from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateProjectState(StatesGroup):
    text_value = State()
    image_value = State()


class CrPrEnum(Enum):
    message_id = 'message_id'
    update_field = 'update_field'
    project_id = 'project_id'
    create = 'create'
