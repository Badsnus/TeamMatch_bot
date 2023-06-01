from aiogram import types

from keyboards.default.main_keyboard import MainKeyboard
from loader import dp


@dp.message_handler(text=MainKeyboard.profile)
async def show_profile(message: types.Message):
    await message.answer('123')
