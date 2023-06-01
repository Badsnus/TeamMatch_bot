from aiogram import types

from keyboards.default.main_keyboard import MainKeyboard
from loader import dp
from services.get_profile_text import get_profile_text
from utils.custom_ctx_data import get_user_from_ctx


@dp.message_handler(text=MainKeyboard.profile)
async def show_profile(message: types.Message) -> None:
    user = get_user_from_ctx()
    await message.answer(get_profile_text(user))
    # with ctx_data as data:
    #     user = data.get('user')
    # print(user)
