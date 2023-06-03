from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_keyboard import MainKeyboard
from keyboards.inline.projects import (
    BACK_TO_PROJECTS_CALL,
    ProjectsKeyboard,
)
from loader import dp
from services.projects import get_projects_main_menu_text


@dp.message_handler(text=MainKeyboard.projects)
async def show_projects_menu(message: types.Message,
                             state: FSMContext) -> None:
    await state.finish()  # DONT TOUCH IT
    await message.answer(
        get_projects_main_menu_text(),
        reply_markup=ProjectsKeyboard.get_keyboard(),
    )


@dp.callback_query_handler(text=BACK_TO_PROJECTS_CALL, state='*')
async def show_projects_menu(call: types.CallbackQuery,
                             state: FSMContext) -> None:
    await state.finish()

    await call.message.edit_text(
        get_projects_main_menu_text(),
        reply_markup=ProjectsKeyboard.get_keyboard(),
    )
