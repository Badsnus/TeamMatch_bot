from aiogram import types

from handlers.users.projects.my_project_retrieve import (
    show_project_retrieve_menu
)
from keyboards.inline.projects import (
    MyProjectsKeyboard,
    MyProjectRetrieveKeyboard,
)
from loader import dp
from models import Project, User


@dp.callback_query_handler(
    text_startswith=MyProjectRetrieveKeyboard.edit_match_call)
async def toggle_match(call: types.CallbackQuery, user: User) -> None:
    project_id = MyProjectRetrieveKeyboard.parse_project_id(call.data)
    project = await Project.get(project_id)

    await project.update(show_for_matching=not project.show_for_matching)

    call.data = MyProjectsKeyboard.generate_call_data(project_id)
    await show_project_retrieve_menu(call, user)
