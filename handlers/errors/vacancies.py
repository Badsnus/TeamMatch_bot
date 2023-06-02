from aiogram import types

from loader import dp
from utils.exceptions import DoNotFindVacancyForSlider


@dp.errors_handler(exception=DoNotFindVacancyForSlider)
async def vacancy_dont_find_plug(update: types.Update,
                                 ex: DoNotFindVacancyForSlider) -> True:
    await update.message.answer(ex.message_for_user)
    return True
