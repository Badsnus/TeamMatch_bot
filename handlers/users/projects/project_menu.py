from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_keyboard import MainKeyboard
from keyboards.inline.project_match import MatchKeyboard
from keyboards.inline.projects import (
    BACK_TO_PROJECTS_CALL,
    ProjectsKeyboard,
)
from loader import dp
from models import Project, User
from services.projects import get_projects_main_menu_text
from utils.delete_message import try_delete_message


@dp.message_handler(text=MainKeyboard.projects)
async def show_projects_menu(message: types.Message,
                             state: FSMContext,
                             user: User) -> None:
    await state.finish()  # DONT TOUCH IT
    # sqlite krivaya, poetomu tak
    notice_count = len(await Project.get_invited_projects(user.id))

    await message.answer(
        get_projects_main_menu_text(),
        reply_markup=ProjectsKeyboard.get_keyboard(notice_count),
    )


@dp.callback_query_handler(text=BACK_TO_PROJECTS_CALL, state='*')
async def show_projects_menu_call(call: types.CallbackQuery,
                                  state: FSMContext,
                                  user: User) -> None:
    await state.finish()

    notice_count = len(await Project.get_invited_projects(user.id))

    await call.message.edit_text(
        get_projects_main_menu_text(),
        reply_markup=ProjectsKeyboard.get_keyboard(notice_count),
    )


@dp.callback_query_handler(text=MatchKeyboard.back_to_project_menu)
async def show_project_menu_from_match(call: types.CallbackQuery,
                                       state: FSMContext, user: User) -> None:
    await try_delete_message(call.message)
    await show_projects_menu(call.message, state, user)
