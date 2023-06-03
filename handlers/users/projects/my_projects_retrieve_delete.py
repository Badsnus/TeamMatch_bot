from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.projects.my_projects import show_projects_list
from keyboards.inline.projects import MyProjectRetrieveKeyboard
from loader import dp
from models import Project, User


# TODO тут конечно надо подтверждение
# ну и удалять тоже странно, скорее архивация или чет такое
@dp.callback_query_handler(
    text_startswith=MyProjectRetrieveKeyboard.delete_project_call)
async def delete_project(call: types.CallbackQuery,
                         state: FSMContext,
                         user: User) -> None:
    project_id = MyProjectRetrieveKeyboard.parse_project_id(call.data)
    await Project.delete_by_id(project_id)

    await call.answer('Проект удален')
    await show_projects_list(call, state, user)
