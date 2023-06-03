from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.exc import IntegrityError

from keyboards.inline.projects import (
    BackToEmployeesList,
    ProjectEmployeesKeyboard,
)
from loader import dp
from models import Employee, InviteToEmployee
from states.projects import AddEmployeeState


# TODO тут надо ограничение на кол-во приглашений
@dp.callback_query_handler(text=ProjectEmployeesKeyboard.add_employee_call)
async def ask_user_id(call: types.CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()

    await call.message.edit_text(
        'Введите ID пользователя\n'
        '<code>(ID указан у пользователя в профиле)</code>',
        reply_markup=BackToEmployeesList.get_keyboard(data.get('project_id')),
    )

    await AddEmployeeState.user_id.set()


@dp.message_handler(state=AddEmployeeState.user_id)
async def send_invite(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.finish()

    project_id = data.get('project_id')
    # MEGA FICHA TODO убрать ее
    try:
        user_id = int(message.text)
    except ValueError:
        user_id = 1

    try:
        already_employee = await Employee.get_by_project_and_user_id(
            project_id,
            user_id,
        )
        if already_employee:
            raise Exception

        inv_emp = InviteToEmployee(project_id=project_id, user_id=user_id)
        await inv_emp.save()

        text = 'Приглашение в проект отправлено'
    except IntegrityError:
        text = 'Вы уже пригласили этого юзера'
    except Exception:  # TODO чет стременое - nado custom error
        text = 'Пользователь уже в проекте'

    await message.answer(
        text,
        reply_markup=BackToEmployeesList.get_keyboard(project_id),
    )
