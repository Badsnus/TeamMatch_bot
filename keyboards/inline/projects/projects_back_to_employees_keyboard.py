from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import MyProjectRetrieveKeyboard


class BackToEmployeesList:
    @classmethod
    def get_keyboard(cls, project_id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text='Вернуться к сотрудникам',
                callback_data=MyProjectRetrieveKeyboard.generate_call_data(
                    MyProjectRetrieveKeyboard.edit_emp_call, project_id,
                ),
            ),
        ]])
        return keyboard
