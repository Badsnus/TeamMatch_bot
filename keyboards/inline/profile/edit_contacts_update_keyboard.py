from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import keyboards.inline.profile as profile_keyboards


class EditContactsUpdateKeyboard:
    callback_delete_contact_prefix = 'profile_delete_contact-'
    callback_update_name_prefix = 'profile_update_contact_name-'
    callback_update_link_prefix = 'profile_update_contact_link-'

    ALL_CALLBACK_PREFIXES = (
        ('Обновить название', callback_update_name_prefix),
        ('Обновить ссылку', callback_update_link_prefix),
        ('Удалить контакт', callback_delete_contact_prefix),
    )

    @classmethod
    def get_contact_id_from_call_data(cls, current_prefix, callback_data: str):
        return callback_data.replace(current_prefix, '')

    @classmethod
    def __generate_callback_edit(cls, current_prefix, contact_id):
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
