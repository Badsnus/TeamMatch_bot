from aiogram import types

from keyboards.default.main_keyboard import MainKeyboard
from keyboards.inline.vacancies import VacanciesSliderKeyboard
from loader import dp


@dp.message_handler(text=MainKeyboard.vacancies)
async def show_vacancies_menu(message: types.Message):
    await message.answer(
        text='Список вакансий',
        reply_markup=VacanciesSliderKeyboard.get_keyboard(0)
    )
