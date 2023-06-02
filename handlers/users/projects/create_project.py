from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.projects import (
    CreateProjectKeyboard,
    ProjectKeyboard,
)
from loader import bot, dp
from services.projects import get_create_project_text, get_fields_values
from states.projects import CreateProjectState, CrPrEnum
from utils.delete_message import try_delete_message


@dp.callback_query_handler(text=ProjectKeyboard.create_project_call)
async def show_project_create_menu(call: types.CallbackQuery,
                                   state: FSMContext) -> None:
    await state.update_data({
        CrPrEnum.message_id.value: call.message.message_id,
    })
    data = await state.get_data()

    await call.message.edit_text(
        text=get_create_project_text(*get_fields_values(data)),
        reply_markup=CreateProjectKeyboard.keyboard,
    )


@dp.callback_query_handler(text_startswith=CreateProjectKeyboard.call_prefix)
async def ask_new_value(call: types.CallbackQuery, state: FSMContext) -> None:
    update_field_name = CreateProjectKeyboard.parse_field_name(call.data)
    await state.update_data({
        CrPrEnum.update_field.value: update_field_name,
    })

    await call.message.edit_text('Введите новое значение для поля')
    await CreateProjectState.value.set()


@dp.message_handler(state=CreateProjectState.value)
async def set_new_value(message: types.Message, state: FSMContext) -> None:
    await state.reset_state(with_data=False)
    data = await state.get_data()
    update_name = data.get(CrPrEnum.update_field.value)
    await state.update_data({update_name: message.text})

    await try_delete_message(message)

    data = await state.get_data()

    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=data.get(CrPrEnum.message_id.value),
        text=get_create_project_text(*get_fields_values(data)),
        reply_markup=CreateProjectKeyboard.keyboard,
    )
