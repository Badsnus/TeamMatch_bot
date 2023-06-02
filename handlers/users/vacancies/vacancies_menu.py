from aiogram import types

from keyboards.default.main_keyboard import MainKeyboard
from loader import dp


@dp.message_handler(text=MainKeyboard.vacancies)
async def show_vacancies_menu(message: types.Message):
    await message.answer(
        text='Список вакансий',
    )
