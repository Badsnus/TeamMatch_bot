from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import keyboards.inline.profile as profile_keyboards
from models.user import UserContact


class UpdateContactsKeyboard:
    callback_delete_contact_prefix = 'profile_delete_contact-'
    callback_update_prefix = 'profile_update_contact_field-'
    callback_update_name_prefix = (
        f'{callback_update_prefix}{UserContact.name.key}-'
    )
    callback_update_link_prefix = (
        f'{callback_update_prefix}{UserContact.link.key}-'
    )

    ALL_CALLBACK_PREFIXES = (
        ('Обновить название', callback_update_name_prefix),
        ('Обновить ссылку', callback_update_link_prefix),
        ('Удалить контакт', callback_delete_contact_prefix),
    )
    FIELD_TRANSLATE = {
        UserContact.name.key: 'название',
        UserContact.link.key: 'ссылка',
    }

    @classmethod
    def get_contact_id_from_call_data(cls,
                                      current_prefix: str,
                                      callback_data: str,
                                      ) -> int:
        return int(callback_data.replace(current_prefix, ''))

    @classmethod
    def get_field_and_id_by_calldata(cls,
                                     callback_data: str,
                                     ) -> tuple[str, str, int]:
        *_, field, contact_id = callback_data.split('-')
        return field, cls.FIELD_TRANSLATE.get(field), int(contact_id)

    @classmethod
    def __generate_callback_edit(cls,
                                 current_prefix: str,
                                 contact_id: int,
                                 ) -> str:
        return current_prefix + str(contact_id)

    @classmethod
    def get_keyboard(cls, contact_id: int) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=2)

        for name, prefix in cls.ALL_CALLBACK_PREFIXES:
            keyboard.insert(InlineKeyboardButton(
                name,
                callback_data=cls.__generate_callback_edit(prefix, contact_id),
            ))

        keyboard.row(InlineKeyboardButton(
            'Вернуться к контактам',
            callback_data=profile_keyboards.ProfileKeyboard.change_contacts,
        ))
        return keyboard
