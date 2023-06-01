from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import RULES_URL


class RegisterKeyboard:
    approve_callback = 'approve_register'

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                'Ознакомиться с правилами',
                url=RULES_URL,
            ),
        ],
        [
            InlineKeyboardButton(
                'Принять правила',
                callback_data=approve_callback,
            ),
        ],
    ])
