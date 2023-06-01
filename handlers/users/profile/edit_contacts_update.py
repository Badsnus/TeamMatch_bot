from aiogram import types

from keyboards.inline.profile import (
    BackToEditContactsMenu,
    EditContactsKeyboard,
    EditContactsUpdateKeyboard,
)
from loader import dp
from models import UserContact
from services.profile_funcs import get_contact_text


@dp.callback_query_handler(
    text_startswith=EditContactsKeyboard.callback_update_prefix)
async def show_change_contact_menu(call: types.CallbackQuery):
    contact_id = EditContactsKeyboard.get_contact_id_from_call_data(call.data)
    contact = await UserContact.get(contact_id)

    await call.message.edit_text(
        get_contact_text(contact),
        reply_markup=EditContactsUpdateKeyboard.get_keyboard(contact_id)
    )


@dp.callback_query_handler(
    text_startswith=EditContactsUpdateKeyboard.callback_delete_contact_prefix)
async def delete_contact(call: types.CallbackQuery):
    contact_id = EditContactsUpdateKeyboard.get_contact_id_from_call_data(
        EditContactsUpdateKeyboard.callback_delete_contact_prefix,
        call.data,
    )
    await UserContact.delete(contact_id)
    await call.message.edit_text(
        'Контакт удален',
        reply_markup=BackToEditContactsMenu.keyboard,
    )
