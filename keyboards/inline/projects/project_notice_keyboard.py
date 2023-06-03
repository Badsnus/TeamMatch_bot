from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import BACK_TO_PROJECTS_CALL
from models import Project


class ProjectNoticeKeyboard:
    check_project_call = 'project_notice_check-'

    @classmethod
    def parse_project_id(cls, call_data: str) -> int:
        return int(call_data.replace(cls.check_project_call, ''))

    @classmethod
    def generate_call_data(cls, project_id: int) -> str:
        return cls.check_project_call + str(project_id)

    @classmethod
    def get_keyboard(cls, project: list[Project]) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=2)
        for project in project:
            keyboard.insert(
                InlineKeyboardButton(
                    project.name,
                    callback_data=cls.generate_call_data(project.id)
                )
            )

        keyboard.row(InlineKeyboardButton(
            'Вернуться назад',
            callback_data=BACK_TO_PROJECTS_CALL,
        ))

        return keyboard
