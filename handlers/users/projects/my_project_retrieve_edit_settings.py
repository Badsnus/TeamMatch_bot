from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.projects.my_project_retrieve import \
    show_project_retrieve_menu
from keyboards.inline.projects import (
    MyProjectEditSettingsKeyboard,
    MyProjectsKeyboard,
    MyProjectRetrieveKeyboard,
)
from loader import dp
from models import Project, User
from models.exceptions import ValidationError
from services.projects import get_create_project_text, get_fields_values, \
    get_fields_items
from states.projects import CrPrEnum


@dp.callback_query_handler(
    text_startswith=MyProjectRetrieveKeyboard.edit_set_call)
async def show_edit_settings_menu(call: types.CallbackQuery,
                                  state: FSMContext) -> None:
    # TODO просто какие-то мега костыли
    # мы юзаем штуку для создания проекта для его редактирования
    # чуток меня класс клавы создания
    project_id = MyProjectRetrieveKeyboard.parse_project_id(call.data)
    data_enum = MyProjectEditSettingsKeyboard.Fields

    project = await Project.get(project_id)

    await state.reset_state(with_data=False)
    await state.update_data({
        CrPrEnum.message_id.value: call.message.message_id,
        CrPrEnum.project_id.value: project_id,
        data_enum.name.value: project.name,
        data_enum.description.value: project.description,
        data_enum.logo_image_id.value: project.logo_image_id,
        data_enum.project_url.value: project.project_url,
        CrPrEnum.create.value: False,
    })
    data = await state.get_data()

    await call.message.edit_text(
        text=get_create_project_text(*get_fields_values(data)),
        reply_markup=MyProjectEditSettingsKeyboard.get_keyboard(),
    )


@dp.callback_query_handler(text=MyProjectEditSettingsKeyboard.back_call)
async def back_to_retrieve_menu(call: types.CallbackQuery,
                                state: FSMContext,
                                user: User) -> None:
    data = await state.get_data()
    await state.finish()

    project_id = data.get(CrPrEnum.project_id.value)
    call.data = MyProjectsKeyboard.generate_call_data(project_id)

    await show_project_retrieve_menu(call, user)


@dp.callback_query_handler(
    text=MyProjectEditSettingsKeyboard.approve_create_call)
async def approve_settings_change_project(call: types.CallbackQuery,
                                          state: FSMContext,
                                          user: User) -> None:
    data = await state.get_data()

    fields = get_fields_items(data)
    project_id = data.get(CrPrEnum.project_id.value)

    try:
        project = await Project.get(project_id)
        await project.update(**fields)

        await state.finish()

    except ValidationError as ex:
        await call.answer(ex.message)
        return

    call.data = MyProjectsKeyboard.generate_call_data(project_id)
    await show_project_retrieve_menu(call, user)
