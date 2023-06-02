from aiogram import types

from keyboards.default.main_keyboard import MainKeyboard
from keyboards.inline.vacancies import VacanciesSliderKeyboard
from loader import dp
from models import Vacancy
from models.exceptions import VacancyNotFound
from services.vacancies import get_vacancy_text


@dp.message_handler(text=MainKeyboard.vacancies)
async def show_vacancies_menu(message: types.Message) -> None:
    vacancies = await Vacancy.get_queryset_by_filters()
    if not vacancies:
        await message.answer(
            '<b>Вакансии и стажировки пока что не доступны :(</b>',
        )
        return
    vacancy = vacancies[0]

    await message.answer_photo(
        photo=vacancy.image_id,
        caption=get_vacancy_text(vacancy),
        reply_markup=VacanciesSliderKeyboard.get_keyboard(vacancy),
    )

# @dp.callback_query_handler(text=MainKeyboard.keyboard)
