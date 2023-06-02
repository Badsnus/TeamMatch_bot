from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .main_profile_keyboard import ProfileKeyboard


class BackToEditExperienceKeyboard:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                'Вернуться к меню опыта',
                callback_data=ProfileKeyboard.change_experience,
            ),
        ],
    ])
