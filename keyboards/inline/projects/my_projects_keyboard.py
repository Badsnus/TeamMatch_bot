from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import BACK_TO_PROJECTS_CALL
from models import Project


class MyProjectKeyboard:
    project_call_prefix = 'projects_my-'

    @classmethod
    def generate_call_data(cls, project_id: int) -> str:
        return f'{cls.project_call_prefix}{project_id}'

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
