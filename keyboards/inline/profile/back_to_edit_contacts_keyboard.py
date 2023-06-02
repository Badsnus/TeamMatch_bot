from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .main_profile_keyboard import ProfileKeyboard


class BackToEditContactsKeyboard:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                'Вернуться к контактам',
                callback_data=ProfileKeyboard.change_contacts,
            ),
        ],
    ])
