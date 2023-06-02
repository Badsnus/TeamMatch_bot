from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_keyboard import MainKeyboard
from keyboards.inline.profile import BACK_TO_PROFILE_CALLBACK, ProfileKeyboard
from loader import dp
from models import User
from services.profile import get_profile_text


@dp.message_handler(text=MainKeyboard.profile)
async def show_profile(message: types.Message, user: User) -> None:
    await message.answer(
        get_profile_text(user),
        reply_markup=ProfileKeyboard.keyboard,
    )


@dp.callback_query_handler(text=BACK_TO_PROFILE_CALLBACK, state='*')
async def show_profile_callback(call: types.CallbackQuery,
                                user: User,
                                state: FSMContext) -> None:
    await state.finish()
    
    await call.message.edit_text(
        get_profile_text(user),
        reply_markup=ProfileKeyboard.keyboard,
    )
