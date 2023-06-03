from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import ProjectsKeyboard
from models import Project


class MyProjectRetrieveKeyboard:
    edit_emp_call = 'projects_my_edit_employees-'
    edit_cand_call = 'projects_my_edit_candidates-'
    edit_set_call = 'projects_my_edit_settings-'
    delete_project_call = 'projects_my_delete'

    leave_call = 'projects_my_leave-'

    @classmethod
    def generate_call_data(cls, prefix: str, project_id: int) -> str:
        return f'{prefix}{project_id}'

    @classmethod
    def get_owner_keyboard(cls, project: Project) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    'Изменить основные настройки',
                    callback_data=cls.generate_call_data(
                        cls.edit_set_call,
                        project.id,
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    'Изменить сотрудников',
                    callback_data=cls.generate_call_data(
                        cls.edit_emp_call,
                        project.id,
                    ),
                ),
                InlineKeyboardButton(
                    'Изменить вакансии',
                    callback_data=cls.generate_call_data(
                        cls.edit_cand_call,
                        project.id,
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    'Удалить проект',
                    callback_data=cls.generate_call_data(
                        cls.delete_project_call,
                        project.id,
                    ),
                ),
            ],
        ])
        return keyboard

    @classmethod
    def get_employee_keyboard(cls, project: Project) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    'Выйти из проекта',
                    callback_data=cls.generate_call_data(
                        cls.leave_call,
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
