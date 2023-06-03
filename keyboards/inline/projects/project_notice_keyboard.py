from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import BACK_TO_PROJECTS_CALL, ProjectsKeyboard
from models import Project


class ProjectNoticeKeyboard:
    prefix = 'project_notice_'
    check_project_call = prefix + 'check-'

    approve_invite_call = prefix + 'approve-'
    reject_invite_call = prefix + 'reject-'

    @classmethod
    def parse_project_id(cls, call_data: str) -> int:
        _, project_id = call_data.split('-')
        return int(project_id)

    @staticmethod
    def generate_call_data(prefix: str, project_id: int) -> str:
        return prefix + str(project_id)

    @staticmethod
    def get_back_button() -> InlineKeyboardButton:
        return InlineKeyboardButton(
            'Вернуться назад',
            callback_data=ProjectsKeyboard.project_notice_call,
        )

    @classmethod
    def get_keyboard(cls, project: list[Project]) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=2)
        for project in project:
            keyboard.insert(
                InlineKeyboardButton(
                    project.name,
                    callback_data=cls.generate_call_data(
                        cls.check_project_call,
                        project.id,
                    ),
                ),
            )

        keyboard.row(InlineKeyboardButton(
            'Вернуться назад',
            callback_data=BACK_TO_PROJECTS_CALL,
        ))

        return keyboard

    @classmethod
    def get_verdict_keyboard(cls, project_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    'Принять приглашение ✅',
                    callback_data=cls.generate_call_data(
                        cls.approve_invite_call,
                        project_id,
                    ),
                ),
                InlineKeyboardButton(
                    'Отклонить приглашение ❌',
                    callback_data=cls.generate_call_data(
                        cls.reject_invite_call,
                        project_id,
                    ),
                ),
            ],
            [
                cls.get_back_button()
            ],
        ])

    @classmethod
    def get_back_keyboard(cls):
        return InlineKeyboardMarkup(inline_keyboard=[[
            cls.get_back_button()
        ]])
