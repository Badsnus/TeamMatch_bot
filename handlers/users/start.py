from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import ShouldHaveArgs
from keyboards.default.main_keyboard import MainKeyboard
from loader import dp


@dp.message_handler(CommandStart(), ShouldHaveArgs())
async def bot_start(message: types.Message) -> None:
    await message.answer(
        'Привет. Я Бот TeamMatch. Я помогу тебе найти тиммейтов для проектов',
        reply_markup=MainKeyboard.keyboard,
    )
