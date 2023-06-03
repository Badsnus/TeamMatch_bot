from aiogram import types

from keyboards.inline.projects import ProjectsKeyboard
from keyboards.inline.project_match import MatchKeyboard
from loader import dp
from models import Project, ProjectMatched, User
from services.project_profile import get_project_profile_text
from utils.delete_message import try_delete_message


@dp.callback_query_handler(text=ProjectsKeyboard.match_project_call)
async def show_project_match_menu(call: types.CallbackQuery,
                                  user: User) -> None:
    # TODO тут 2 запроса, потому что алхимия херня какая-то или я просто клоун
    project_id = await ProjectMatched.get_project_without_match(user.id)

    if project_id is None:
        await call.answer('У вас нет непросмотренных проектов')
        return

    project = await Project.get(project_id, do_join=True)

    await call.message.answer(
        get_project_profile_text(project),
        reply_markup=MatchKeyboard.get_keyboard(project_id),
    )
    await try_delete_message(call.message)
