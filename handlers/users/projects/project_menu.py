from aiogram import types

from keyboards.default.main_keyboard import MainKeyboard
from keyboards.inline.projects import ProjectKeyboard
from loader import dp


@dp.message_handler(text=MainKeyboard.projects)
async def show_projects_menu(message: types.Message):
    await message.answer(
        'Проекты',
        reply_markup=ProjectKeyboard.keyboard,
    )
