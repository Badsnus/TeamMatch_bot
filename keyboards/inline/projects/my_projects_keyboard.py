from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import BACK_TO_PROJECTS_CALL
from models import Project


class MyProjectsKeyboard:
    call_prefix = 'projects_my_retrieve-'

    @classmethod
    def parse_project_id(cls, call_data: str) -> int:
        return int(call_data.replace(cls.call_prefix, ''))

    @classmethod
    def generate_call_data(cls, project_id: int) -> str:
        return f'{cls.call_prefix}{project_id}'

    @classmethod
    def get_keyboard(cls, projects: list[Project]) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=2)
        for project in projects:
            keyboard.insert(InlineKeyboardButton(
                project.name,
                callback_data=cls.generate_call_data(project.id),
            ))

        keyboard.row(InlineKeyboardButton(
            'Вернуться к проектам',
            callback_data=BACK_TO_PROJECTS_CALL,
        ))

        return keyboard
