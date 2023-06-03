from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_keyboard import MainKeyboard
from keyboards.inline.projects import (
    BACK_TO_PROJECTS_CALL,
    ProjectsKeyboard,
)
from loader import dp
from models import InviteToEmployee, User
from services.projects import get_projects_main_menu_text


@dp.message_handler(text=MainKeyboard.projects)
async def show_projects_menu(message: types.Message,
                             state: FSMContext,
                             user: User) -> None:
    await state.finish()  # DONT TOUCH IT

    notice_count = await InviteToEmployee.get_notice_count_by_user(user.id)

    await message.answer(
        get_projects_main_menu_text(),
        reply_markup=ProjectsKeyboard.get_keyboard(notice_count),
    )


@dp.callback_query_handler(text=BACK_TO_PROJECTS_CALL, state='*')
async def show_projects_menu(call: types.CallbackQuery,
                             state: FSMContext,
                             user: User) -> None:
    await state.finish()

    notice_count = await InviteToEmployee.get_notice_count_by_user(user.id)

    await call.message.edit_text(
        get_projects_main_menu_text(),
        reply_markup=ProjectsKeyboard.get_keyboard(notice_count),
    )
