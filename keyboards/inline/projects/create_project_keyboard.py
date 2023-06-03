from enum import Enum

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import BACK_TO_PROJECTS_CALL


class CreateProjectKeyboard:
    class Fields(Enum):
        name = 'name'
        description = 'description'
        logo_image_id = 'logo_image_id'
        project_url = 'project_url'

    call_prefix = 'project_create'

    call_field_prefix = call_prefix + '_field-'

    edit_name_call = call_field_prefix + Fields.name.value
    edit_description_call = call_field_prefix + Fields.description.value
    edit_logo_call = call_prefix + '_photo-' + Fields.logo_image_id.value
    edit_project_url_call = call_field_prefix + Fields.project_url.value

    create_text = 'Создать проект'
    approve_create_call = call_prefix + '_approve'

    back_text = 'Вернуться к проектам'
    back_call = BACK_TO_PROJECTS_CALL

    @classmethod
    def parse_field_name(cls, callback_data: str) -> str:
        return callback_data.replace(cls.call_field_prefix, '')

    @classmethod
    def get_keyboard(cls) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    'Изменить название',
                    callback_data=cls.edit_name_call,
                ),
                InlineKeyboardButton(
                    'Изменить описание',
                    callback_data=cls.edit_description_call,
                ),
            ],
            [
                InlineKeyboardButton(
                    'Изменить логотип',
                    callback_data=cls.edit_logo_call,
                ),
                InlineKeyboardButton(
                    'Изменить ссылку',
                    callback_data=cls.edit_project_url_call,
                ),
            ],
            [
                InlineKeyboardButton(
                    cls.create_text,
                    callback_data=cls.approve_create_call,
                ),
            ],
            [
                InlineKeyboardButton(
                    cls.back_text,
                    callback_data=cls.back_call,
                ),
            ],
        ])
