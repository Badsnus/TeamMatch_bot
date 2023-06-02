from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .main_profile_keyboard import ProfileKeyboard


class BackToEditSkillsKeyboard:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                'Вернуться к меню скиллов',
                callback_data=ProfileKeyboard.change_skills,
            ),
        ],
    ])
