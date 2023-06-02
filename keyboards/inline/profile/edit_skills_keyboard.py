from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.profile import BACK_TO_PROFILE_CALLBACK


class EditSkillsKeyboard:
    delete_skills_menu = 'profile_skills_delete_menu'
    add_skill_call = 'profile_skills_add'

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                'Добавить скиллы',
                callback_data=add_skill_call,
            ),
        ],
        [
            InlineKeyboardButton(
                'Меню удаление скиллов',
                callback_data=delete_skills_menu,
            ),
        ],
        [
            InlineKeyboardButton(
                'Вернуться в профиль',
                callback_data=BACK_TO_PROFILE_CALLBACK,
            ),
        ],
    ])
