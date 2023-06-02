from aiogram import types

from keyboards.inline.projects import (
    CreateProjectKeyboard,
    ProjectKeyboard,
)
from loader import dp
from services.projects import get_create_project_text


@dp.callback_query_handler(text=ProjectKeyboard.create_project_call)
async def show_project_create_menu(call: types.CallbackQuery) -> None:
    text = get_create_project_text('', '', '', '')
    await call.message.edit_text(
        text,
        reply_markup=CreateProjectKeyboard.keyboard,
    )
