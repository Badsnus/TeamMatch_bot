from aiogram import types

from keyboards.inline.projects import MyProjectsKeyboard, ProjectsKeyboard
from loader import dp
from models import Project, User


@dp.callback_query_handler(text=ProjectsKeyboard.my_projects_call)
async def show_projects_list(call: types.CallbackQuery, user: User) -> None:
    projects = await Project.get_projects_by_user(user.id)
    await call.message.edit_text(
        'Выберите проект для редактирования',
        reply_markup=MyProjectsKeyboard.get_keyboard(projects),
    )
