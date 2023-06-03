from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import ProjectsKeyboard
from models import Project


class MyProjectRetrieveKeyboard:
    edit_call_prefix = 'projects_my_edit-'
    leave_call_prefix = 'projects_my_leave-'

    @classmethod
    def generate_call_data(cls, prefix: str, project_id: int) -> str:
        return f'{prefix}{project_id}'

    @classmethod
    def get_owner_keyboard(cls, project: Project) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        return keyboard

    @classmethod
    def get_employee_keyboard(cls, project: Project) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    'Выйти из проекта',
                    callback_data=cls.generate_call_data(
                        cls.leave_call_prefix,
                        project.id,
                    ),
                ),
            ],
        ])
        return keyboard

    @classmethod
    def get_keyboard(cls,
                     project: Project,
                     is_owner: bool) -> InlineKeyboardMarkup:
        keyboard = (
            cls.get_owner_keyboard(project) if is_owner
            else cls.get_employee_keyboard(project)
        )
        keyboard.row(InlineKeyboardButton(
            text='Вернуться к моим проектам',
            callback_data=ProjectsKeyboard.my_projects_call,
        ))

        return keyboard
