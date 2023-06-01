from aiogram import types

from keyboards.inline.register_keyboard import RegisterKeyboard
from loader import dp, session
from models import User


@dp.callback_query_handler(text=RegisterKeyboard.approve_callback)
async def registrate_user(callback: types.CallbackQuery) -> None:
    print(123)
    user = await User.create(
        name=callback.from_user.first_name,
        telegram_id=callback.from_user.id,
        telegram_username=callback.from_user.username,
    )
    print(user)
