from aiogram import types

from keyboards.default.main_keyboard import MainKeyboard
from keyboards.inline.profile_keyboards import ProfileKeyboard
from loader import dp
from services.get_profile_text import get_profile_text
from utils.custom_ctx_data import get_user_from_ctx


@dp.message_handler(text=MainKeyboard.profile)
async def show_profile(message: types.Message) -> None:
    user = get_user_from_ctx()
    await message.answer(
        get_profile_text(user),
        reply_markup=ProfileKeyboard.keyboard,
    )
