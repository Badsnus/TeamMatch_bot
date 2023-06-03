from aiogram import types

from keyboards.inline.projects import (
    MyProjectsKeyboard,
    MyProjectRetrieveKeyboard,
)
from loader import dp
from models import Employee, Project, User
from services.projects import get_project_retrieve_text


@dp.callback_query_handler(text_startswith=MyProjectsKeyboard.call_prefix)
async def show_project_retrieve_menu(call: types.CallbackQuery,
                                     user: User) -> None:
    project_id = MyProjectsKeyboard.parse_project_id(call.data)
    project = await Project.get(project_id, do_join=True)
    user_is_owner = await Employee.check_user_is_owner(project_id, user.id)

    await call.message.edit_text(
        get_project_retrieve_text(project),
        reply_markup=MyProjectRetrieveKeyboard.get_keyboard(
            project,
            user_is_owner,
        ),
    )
