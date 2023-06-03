from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.projects import (
    BackToCreateProjectKeyboard,
    BackToMainProjectsKeyboard,
    CreateProjectKeyboard,
    MyProjectEditSettingsKeyboard,
    ProjectsKeyboard,
)
from models import Project, User
from models.exceptions import ValidationError
from loader import bot, dp
from services.projects import (
    get_create_project_text,
    get_fields_items,
    get_fields_values,
)
from states.projects import CreateProjectState, CrPrEnum
from utils.delete_message import try_delete_message


@dp.callback_query_handler(text=ProjectsKeyboard.create_project_call,
                           state='*')
async def show_project_create_menu(call: types.CallbackQuery,
                                   state: FSMContext) -> None:
    # TODO а вот и эти мега костыли
    await state.reset_state(with_data=False)
    data = await state.get_data()
    data.update({CrPrEnum.message_id.value: call.message.message_id})
    if CrPrEnum.create.value not in data:
        data.update({CrPrEnum.create.value: True})

    await state.update_data(data)

    keyboard_class = (
        CreateProjectKeyboard if data[CrPrEnum.create.value]
        else MyProjectEditSettingsKeyboard
    )

    await call.message.edit_text(
        text=get_create_project_text(*get_fields_values(data)),
        reply_markup=keyboard_class.get_keyboard(),
    )


@dp.callback_query_handler(
    text_startswith=CreateProjectKeyboard.call_field_prefix)
async def ask_new_value(call: types.CallbackQuery, state: FSMContext) -> None:
    update_field_name = CreateProjectKeyboard.parse_field_name(call.data)
    await state.update_data({
        CrPrEnum.update_field.value: update_field_name,
    })

    await call.message.edit_text(
        'Введите новое значение для поля',
        reply_markup=BackToCreateProjectKeyboard.keyboard,
    )
    await CreateProjectState.text_value.set()


async def delete_message_and_send_update_menu(
        data: dict,
        message: types.Message) -> None:
    await try_delete_message(message)

    keyboard_class = (
        CreateProjectKeyboard if data[CrPrEnum.create.value]
        else MyProjectEditSettingsKeyboard
    )

    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=data.get(CrPrEnum.message_id.value),
        text=get_create_project_text(*get_fields_values(data)),
        reply_markup=keyboard_class.get_keyboard(),
    )


@dp.message_handler(state=CreateProjectState.text_value)
async def set_new_value(message: types.Message, state: FSMContext) -> None:
    # TODO мб стоит это отсюда вынести, но хз, так как не хочется
    # куда-то стейт передавать
    await state.reset_state(with_data=False)
    data = await state.get_data()
    update_name = data.get(CrPrEnum.update_field.value)
    data[update_name] = message.text
    await state.update_data({update_name: message.text})

    await delete_message_and_send_update_menu(data, message)


@dp.callback_query_handler(text=CreateProjectKeyboard.edit_logo_call)
async def edit_logo(call: types.CallbackQuery) -> None:
    await call.message.edit_text(
        'Пришлите логотип проекта (нужно прислать именно фото, не файл)',
        reply_markup=BackToCreateProjectKeyboard.keyboard,
    )
    await CreateProjectState.image_value.set()


@dp.message_handler(content_types=types.ContentTypes.PHOTO,
                    state=CreateProjectState.image_value)
async def set_logo(message: types.Message, state: FSMContext) -> None:
    await state.reset_state(with_data=False)
    data = await state.get_data()
    data[
        CreateProjectKeyboard.Fields.logo_image_id.value
    ] = message.photo[-1].file_id
    await state.update_data(data)

    await delete_message_and_send_update_menu(data, message)


@dp.callback_query_handler(text=CreateProjectKeyboard.approve_create_call)
async def create_project(call: types.CallbackQuery,
                         user: User,
                         state: FSMContext) -> None:
    data = get_fields_items(await state.get_data())

    try:
        project = Project(**data)
        await project.create_project_with_owner(user)

        await state.finish()

    except ValidationError as ex:
        await call.answer(ex.message)
        return
    # TODO мб тут редирект на страницу проекта?
    await call.message.edit_text(
        'Проект создан',
        reply_markup=BackToMainProjectsKeyboard.keyboard,
    )
