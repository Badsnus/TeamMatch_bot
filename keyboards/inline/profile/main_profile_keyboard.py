from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class ProfileKeyboard:
    change_name = 'profile_change_name'
    change_specialization = 'profile_change_specialization'
    change_contacts = 'profile_change_contacts'
    change_experience = 'profile_change_experience'

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                'Изменить имя',
                callback_data=change_name,
            ),
        ],
        [
            InlineKeyboardButton(
                'Изменить специализацию',
                callback_data=change_specialization,
            ),
        ],
        [
            InlineKeyboardButton(
                'Изменить контакты',
                callback_data=change_contacts,
            ),
        ],
        [
            InlineKeyboardButton(
                'Изменить опыт работы',
                callback_data=change_experience
            )
        ],
    ])
