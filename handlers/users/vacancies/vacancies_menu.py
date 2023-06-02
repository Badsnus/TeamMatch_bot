from aiogram import types

from keyboards.default.main_keyboard import MainKeyboard
from keyboards.inline.vacancies import VacanciesSliderKeyboard
from loader import dp
from services.vacancies import (
    get_vacancy_text,
    get_vacancy_and_offset, get_vacancy_start_index,
)


@dp.message_handler(text=MainKeyboard.vacancies)
async def show_vacancies_menu(message: types.Message) -> None:
    vacancy_id = await get_vacancy_start_index()

    vacancy, need_left, need_right = await get_vacancy_and_offset(
        direction=VacanciesSliderKeyboard.RIGHT,
        vacancy_id=vacancy_id,
        need_left=False,
    )

    await message.answer_photo(
        photo=vacancy.image_id,
        caption=get_vacancy_text(vacancy),
        reply_markup=VacanciesSliderKeyboard.get_keyboard(
            vacancy=vacancy,
            need_left=need_left,
            need_right=need_right,
        ),
    )


@dp.callback_query_handler(
    text_startswith=VacanciesSliderKeyboard.slider_callback)
async def show_vacancy(call: types.CallbackQuery) -> None:
    direction, vacancy_id = VacanciesSliderKeyboard.parse_callback(call.data)

    vacancy, need_left, need_right = await get_vacancy_and_offset(
        direction=direction,
        vacancy_id=vacancy_id,
    )

    await call.message.edit_media(
        media=types.InputMediaPhoto(
            media=vacancy.image_id,
            caption=get_vacancy_text(vacancy),
        ),
        reply_markup=VacanciesSliderKeyboard.get_keyboard(
            vacancy=vacancy,
            need_left=need_left,
            need_right=need_right,
        ),
    )
