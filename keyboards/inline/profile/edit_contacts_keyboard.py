from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.profile import BACK_TO_PROFILE_CALLBACK
from models import UserContact


class EditContactsKeyboard:
    callback_update_prefix = 'profile_update_contact-'
    callback_create_prefix = 'profile_create_contact'

    @classmethod
    def get_contact_id_from_call_data(cls, callback_data: str):
        return callback_data.replace(cls.callback_update_prefix, '')

    @classmethod
    def __generate_callback_edit(cls, contact_id):
        return cls.callback_update_prefix + str(contact_id)

    @classmethod
    def get_keyboard(cls,
                     contacts: list[UserContact]) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=2)

        for contact in contacts:
            keyboard.insert(
                InlineKeyboardButton(
                    contact.name,
                    callback_data=cls.__generate_callback_edit(contact.id),
                ),
            )

        keyboard.row(InlineKeyboardButton(
            'Добавить контакт',
            callback_data=cls.callback_create_prefix,
        ))
        keyboard.row(InlineKeyboardButton(
            'Вернуться в профиль',
            callback_data=BACK_TO_PROFILE_CALLBACK,
        ))
        return keyboard
