from aiogram import types

from keyboards.inline.projects import ProjectsKeyboard
from keyboards.inline.project_match import MatchKeyboard
from loader import dp
from models import Project, ProjectMatched, User
from services.project_profile import get_project_profile_text
from utils.delete_message import try_delete_message


async def get_project_or_send_er_message(call: types.CallbackQuery,
                                         user_id: int) -> Project | None:
    # TODO тут 2 запроса, потому что алхимия херня какая-то или я просто клоун
    project_id = await ProjectMatched.get_project_without_match(user_id)

    if project_id is None:
        await call.answer('У вас нет непросмотренных проектов')
        return

    project = await Project.get(project_id, do_join=True)
    return project


@dp.callback_query_handler(text=ProjectsKeyboard.match_project_call)
async def show_project_match_menu(call: types.CallbackQuery,
                                  user: User) -> None:
    project = await get_project_or_send_er_message(call, user.id)
    if project:
        await call.message.answer_photo(
            caption=get_project_profile_text(project),
            photo=project.logo_image_id,
            reply_markup=MatchKeyboard.get_keyboard(project.id),
        )
        await try_delete_message(call.message)


@dp.callback_query_handler(text_startswith=MatchKeyboard.give_info_call)
async def give_info_about_project(call: types.CallbackQuery,
                                  user: User) -> None:
    project_id = MatchKeyboard.parse_project_id(call.data)
    project = await Project.get(project_id, do_join=True)

    await ProjectMatched(project_id=project_id, user_id=user.id).save()

    await call.message.edit_caption(
        '<b>Оставляю тебе этот проект на память</b> #project' +
        get_project_profile_text(project),
    )


@dp.callback_query_handler(text_startswith=MatchKeyboard.next_project_call)
async def match_project(call: types.CallbackQuery, user: User) -> None:
    project_id = MatchKeyboard.parse_project_id(call.data)
    await ProjectMatched(project_id=project_id, user_id=user.id).save()

    project = await get_project_or_send_er_message(call, user.id)
    if project:
        await call.message.edit_media(
            media=types.InputMediaPhoto(
                caption=get_project_profile_text(project),
                media=project.logo_image_id,
            ),
            reply_markup=MatchKeyboard.get_keyboard(project.id),
        )
    else:
        await try_delete_message(call.message)
