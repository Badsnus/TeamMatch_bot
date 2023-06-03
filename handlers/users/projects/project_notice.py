from aiogram import types

from keyboards.inline.projects import ProjectNoticeKeyboard, ProjectsKeyboard
from loader import dp
from models import Project, User


@dp.callback_query_handler(text=ProjectsKeyboard.project_notice_call)
async def show_notice_list(call: types.CallbackQuery, user: User) -> None:
    projects = await Project.get_invited_projects(user.id)

    await call.message.edit_text(
        'Список проектов, в которые вас пригласили',
        reply_markup=ProjectNoticeKeyboard.get_keyboard(projects),
    )
