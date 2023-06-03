from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import MyProjectRetrieveKeyboard


class ProjectEmployeeRetrieveKeyboard:
    edit_role_call = 'project_employee_retrieve_edit_role'
    delete_call = 'project_employee_retrieve_delete'

    @classmethod
    def get_keyboard(cls, project_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Редактировать роль',
                    callback_data=cls.edit_role_call
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Удалить сотрудника',
                    callback_data=cls.delete_call,
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Вернуться ко всем сотрудникам',
                    callback_data=MyProjectRetrieveKeyboard.generate_call_data(
                        MyProjectRetrieveKeyboard.edit_emp_call, project_id,
                    ),
                ),
            ],
        ])
