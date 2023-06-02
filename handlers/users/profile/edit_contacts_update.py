from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.profile import (
    BackToEditContactsKeyboard,
    BackToUpdateContactKeyboard,
    EditContactsKeyboard,
    UpdateContactsKeyboard,
)
from loader import dp
from models import UserContact
from services.profile import get_contact_text
from states.profile import UpdateContactFieldState


@dp.callback_query_handler(
    text_startswith=EditContactsKeyboard.callback_update_prefix, state='*')
async def show_change_contact_menu(call: types.CallbackQuery,
                                   state: FSMContext) -> None:
    await state.finish()

    contact_id = EditContactsKeyboard.get_contact_id_from_call_data(call.data)
    contact = await UserContact.get(contact_id)

    await call.message.edit_text(
        get_contact_text(contact),
        reply_markup=UpdateContactsKeyboard.get_keyboard(contact_id)
    )


@dp.callback_query_handler(
    text_startswith=UpdateContactsKeyboard.callback_delete_contact_prefix)
async def delete_contact(call: types.CallbackQuery) -> None:
    contact_id = UpdateContactsKeyboard.get_contact_id_from_call_data(
        UpdateContactsKeyboard.callback_delete_contact_prefix,
        call.data,
    )
    await UserContact.delete(contact_id)
    await call.message.edit_text(
        'Контакт удален',
        reply_markup=BackToEditContactsKeyboard.keyboard,
    )


@dp.callback_query_handler(
    text_startswith=UpdateContactsKeyboard.callback_update_prefix)
async def ask_new_contact(call: types.CallbackQuery,
                          state: FSMContext) -> None:
    field_name, field_translate, contact_id = (
        UpdateContactsKeyboard.get_field_and_id_by_calldata(call.data)
    )
    await state.update_data(field_name=field_name, contact_id=contact_id)
    await UpdateContactFieldState.value.set()

    await call.message.edit_text(
        f'Пришлите значение для поля {field_translate}',
        reply_markup=BackToUpdateContactKeyboard.get_keyboard(contact_id),
    )


@dp.message_handler(state=UpdateContactFieldState.value)
async def update_contact(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.finish()
    contact_id, field_name = data['contact_id'], data['field_name']
    await UserContact.update(contact_id, **{field_name: message.text})

    await message.answer(
        'Контакт изменен',
        reply_markup=BackToUpdateContactKeyboard.get_keyboard(contact_id),
    )
