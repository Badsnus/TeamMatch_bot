from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.profile import BACK_TO_PROFILE_CALLBACK
from models import UserExperience


class EditExperienceKeyboard:
    add_call = 'profile_experience_add'
    edit_call_prefix = 'profile_experience_edit-'

    @classmethod
    def _generate_callback_data(cls, experience_id: int) -> str:
        return cls.edit_call_prefix + str(experience_id)

    @classmethod
    def get_keyboard(cls,
                     experience: list[UserExperience],
                     ) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=3)
        for exp in experience:
            keyboard.insert(
                InlineKeyboardButton(
                    text='Изменить ' + exp.name[:10],
                    callback_data=cls._generate_callback_data(exp.id),
                ),
            )

        keyboard.row(
            InlineKeyboardButton(
                text='Добавить опыт',
                callback_data=cls.add_call,
            ),
        )
        keyboard.row(
            InlineKeyboardButton(
                text='Вернуться в профиль',
                callback_data=BACK_TO_PROFILE_CALLBACK,
            ),
        )
        return keyboard
