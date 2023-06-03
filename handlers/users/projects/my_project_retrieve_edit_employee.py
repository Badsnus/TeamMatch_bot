from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.projects import (
    MyProjectRetrieveKeyboard,
    ProjectEmployeeRetrieveKeyboard,
)
from keyboards.inline.projects import ProjectEmployeesKeyboard

from loader import dp
from models import Project, Employee
from services.projects import get_employee_text
from states.projects import UpdateRoleState


@dp.callback_query_handler(
    text_startswith=MyProjectRetrieveKeyboard.edit_emp_call, state='*')
async def show_emp_menu(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.finish()

    project_id = MyProjectRetrieveKeyboard.parse_project_id(call.data)
    await state.update_data(project_id=project_id)

    project = await Project.get(project_id, do_join=True)

    await call.message.edit_text(
        'Выберите сотрудника для редактирования',
        reply_markup=ProjectEmployeesKeyboard.get_keyboard(project.employees),
    )


@dp.callback_query_handler(
    text_startswith=ProjectEmployeesKeyboard.edit_employee_call, state='*')
async def show_employee_retrieve_menu(call: types.CallbackQuery,
                                      state: FSMContext) -> None:
    await state.reset_state(with_data=False)

    employee_id = ProjectEmployeesKeyboard.parse_employee_id(call.data)
    employee = await Employee.get(employee_id)

    await state.update_data(employee_id=employee_id)

    await call.message.edit_text(
        get_employee_text(employee),
        reply_markup=ProjectEmployeeRetrieveKeyboard.get_keyboard(
            employee.project_id,
        ),
    )


@dp.callback_query_handler(text=ProjectEmployeeRetrieveKeyboard.edit_role_call)
async def ask_new_role(call: types.CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    employee_id = data.get('employee_id')

    await call.message.edit_text(
        'Введите новую роль',
        reply_markup=ProjectEmployeesKeyboard.get_back_keyboard(employee_id),
    )

    await UpdateRoleState.role.set()


@dp.message_handler(state=UpdateRoleState.role)
async def update_role(message: types.Message, state: FSMContext) -> None:
    await state.reset_state(with_data=False)
    data = await state.get_data()

    employee_id = data.get('employee_id')  # TODo эт бы так не вшивать...
    employee = await Employee.get(employee_id)
    await employee.update(role=message.text)

    await message.answer(
        get_employee_text(employee),
        reply_markup=ProjectEmployeeRetrieveKeyboard.get_keyboard(
            employee.project_id,
        ),
    )


@dp.callback_query_handler(text=ProjectEmployeeRetrieveKeyboard.delete_call)
async def delete_employee(call: types.CallbackQuery,
                          state: FSMContext) -> None:
    data = await state.get_data()
    await state.reset_state(with_data=False)

    employee_id = data.get('employee_id')

    employee = await Employee.get(employee_id)

    if employee.is_owner:
        await call.answer('Вы не можете удалить себя')
        return

    await Employee.delete_by_id(data.get('employee_id'))

    call.data = MyProjectRetrieveKeyboard.generate_call_data(
        prefix=MyProjectRetrieveKeyboard.edit_emp_call,
        project_id=data.get('project_id'),
    )

    await call.answer('Сотрудника удален')
    await show_emp_menu(call, state)
