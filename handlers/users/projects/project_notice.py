from aiogram import types
from aiogram.utils.exceptions import BadRequest

from keyboards.inline.projects import ProjectNoticeKeyboard, ProjectsKeyboard
from loader import dp
from models import Employee, InviteToEmployee, Project, User
from services.project_profile import get_project_profile_text
from utils.delete_message import try_delete_message


@dp.callback_query_handler(text=ProjectsKeyboard.project_notice_call)
async def show_notice_list(call: types.CallbackQuery, user: User) -> None:
    projects = await Project.get_invited_projects(user.id)
    text = 'Список проектов, в которые вас пригласили'
    keyboard = ProjectNoticeKeyboard.get_keyboard(projects)
    try:
        await call.message.edit_text(text, reply_markup=keyboard)

    except BadRequest:
        await call.message.answer(text, reply_markup=keyboard)
        await try_delete_message(call.message)


@dp.callback_query_handler(
    text_startswith=ProjectNoticeKeyboard.check_project_call)
async def show_project_profile(call: types.CallbackQuery) -> None:
    project_id = ProjectNoticeKeyboard.parse_project_id(call.data)
    project = await Project.get(project_id, do_join=True)

    await call.message.answer_photo(
        photo=project.logo_image_id,
        caption=get_project_profile_text(project),
        reply_markup=ProjectNoticeKeyboard.get_verdict_keyboard(project_id),
    )
    await try_delete_message(call.message)


@dp.callback_query_handler(
    text_startswith=ProjectNoticeKeyboard.approve_invite_call)
async def approve_invite(call: types.CallbackQuery, user: User) -> None:
    await try_delete_message(call.message)

    project_id = ProjectNoticeKeyboard.parse_project_id(call.data)
    employee = await Employee.get_by_project_and_user_id(
        project_id=project_id,
        user_id=user.id,
    )
    keyboard = ProjectNoticeKeyboard.get_back_keyboard()

    if employee:
        await call.message.answer('Вы уже в проекте', reply_markup=keyboard)
        return

    # TODo уже похер, но надо бы транзакцию
    await Employee(user_id=user.id, project_id=project_id).save()
    await InviteToEmployee.delete(project_id=project_id, user_id=user.id)

    await call.message.answer(
        'Вы приняли приглашение в проект',
        reply_markup=keyboard,
    )
