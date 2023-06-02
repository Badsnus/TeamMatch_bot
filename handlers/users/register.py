from aiogram import types

from handlers.users.start import bot_start
from keyboards.inline.register_keyboard import RegisterKeyboard
from loader import dp
from models import User
from utils.delete_message import try_delete_message


@dp.callback_query_handler(text=RegisterKeyboard.approve_callback)
async def registrate_user(callback: types.CallbackQuery) -> None:
    await User.create(
        name=callback.from_user.first_name,
        telegram_id=callback.from_user.id,
        telegram_username=callback.from_user.username,
    )
    await try_delete_message(callback.message)
    await bot_start(callback.message)
