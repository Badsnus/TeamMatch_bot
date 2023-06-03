from aiogram import types

from keyboards.inline.projects import ProjectsKeyboard
from loader import dp


@dp.callback_query_handler(text=ProjectsKeyboard.match_project_call)
async def show_project_match_menu(call: types.CallbackQuery) -> None:
    ...
