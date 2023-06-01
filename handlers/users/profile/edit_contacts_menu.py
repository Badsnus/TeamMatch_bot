from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.profile import (
    EditContactsKeyboard,
    ProfileKeyboard,
)
from loader import dp
from models import User


@dp.callback_query_handler(text=ProfileKeyboard.change_contacts, state='*')
async def show_change_contacts_menu(call: types.CallbackQuery,
                                    user: User, state: FSMContext) -> None:
    await state.finish()
    await call.message.edit_text(
        'Меню контактов',
        reply_markup=EditContactsKeyboard.get_keyboard(user.contacts),
    )
