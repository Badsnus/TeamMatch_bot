from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import BACK_TO_MY_PROJECT_RETRIEVE
from models import Employee


class ProjectEmployeesKeyboard:
    edit_employee_call = 'my_projects_employee_edit-'
    add_employee_call = 'my_projects_employee_add'

    @classmethod
    def parse_employee_id(cls, call_data: str) -> int:
        return int(call_data.replace(cls.edit_employee_call, ''))

    @classmethod
    def get_call_data(cls, employee_id: int) -> str:
        return f'{cls.edit_employee_call}{employee_id}'

    @classmethod
    def get_keyboard(cls, employees: list[Employee]) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        for employee in employees:
            keyboard.insert(
                InlineKeyboardButton(
                    employee.user.name,
                    callback_data=cls.get_call_data(employee.id),
                ),
            )
        keyboard.row(InlineKeyboardButton(
            'Добавить сотрудника',
            callback_data=cls.add_employee_call,
        ))
        keyboard.row(InlineKeyboardButton(
            'Вернуться назад',
            callback_data=BACK_TO_MY_PROJECT_RETRIEVE,
        ))

        return keyboard
