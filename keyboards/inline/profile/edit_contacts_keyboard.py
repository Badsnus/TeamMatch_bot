from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.profile import BACK_TO_PROFILE_CALLBACK
from models import UserContact


class UpdateContactMixin:
    callback_update_prefix = 'profile_update_contact-'

    @classmethod
    def get_contact_id_from_call_data(cls, callback_data: str) -> int:
        return int(callback_data.replace(cls.callback_update_prefix, ''))

    @classmethod
    def _generate_callback_edit(cls, contact_id: int) -> str:
        return cls.callback_update_prefix + str(contact_id)


class EditContactsKeyboard(UpdateContactMixin):
    callback_create_prefix = 'profile_create_contact'

    @classmethod
    def get_keyboard(cls,
                     contacts: list[UserContact]) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=2)

        for contact in contacts:
            keyboard.insert(
                InlineKeyboardButton(
                    contact.name,
                    callback_data=cls._generate_callback_edit(contact.id),
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


class BackToUpdateContactKeyboard(UpdateContactMixin):
    @classmethod
    def get_keyboard(cls, contact_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                'Обратно к контакту',
                callback_data=cls._generate_callback_edit(contact_id),
            ),
        ]])
