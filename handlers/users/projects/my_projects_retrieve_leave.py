from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.projects.my_projects import show_projects_list
from keyboards.inline.projects import MyProjectRetrieveKeyboard
from loader import dp
from models import Employee, User


@dp.callback_query_handler(
    text_startswith=MyProjectRetrieveKeyboard.leave_call)
async def delete_project(call: types.CallbackQuery,
                         state: FSMContext,
                         user: User) -> None:
    project_id = MyProjectRetrieveKeyboard.parse_project_id(call.data)
    await Employee.delete_by_user_and_project_id(
        user.id,
        project_id,
    )

    await call.answer('Вы вышли из проекта')
    await show_projects_list(call, state, user)
