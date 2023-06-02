from enum import Enum

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import BACK_TO_PROJECTS_CALL


class CreateProjectKeyboard:
    class Fields(Enum):
        name = 'name'
        description = 'description'
        logo_image_id = 'logo_image_id'
        project_url = 'project_url'

    call_prefix = 'project_create_'

    edit_name_call = call_prefix + Fields.name.value
    edit_description_call = call_prefix + Fields.description.value
    edit_logo_call = call_prefix + Fields.logo_image_id.value
    edit_project_url_call = call_prefix + Fields.project_url.value

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                'Изменить название',
                callback_data=edit_name_call,
            ),
            InlineKeyboardButton(
                'Изменить описание',
                callback_data=edit_description_call,
            ),
        ],
        [
            InlineKeyboardButton(
                'Изменить логотип',
                callback_data=edit_logo_call,
            ),
            InlineKeyboardButton(
                'Изменить ссылку',
                callback_data=edit_project_url_call,
            ),
        ],
        [
            InlineKeyboardButton(
                'Вернуться к проектам',
                callback_data=BACK_TO_PROJECTS_CALL,
            ),
        ],
    ])
