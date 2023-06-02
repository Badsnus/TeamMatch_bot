from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.profile import (
    BackToEditExperienceRetrieveKeyboard,
    EditExperienceKeyboard,
    EditExperienceRetrieveKeyboard,
)
from loader import dp
from models import UserExperience
from services.profile import get_experience_retrieve_text
from states.profile import ExperienceRetrieveState


@dp.callback_query_handler(
    text_startswith=EditExperienceKeyboard.edit_call_prefix, state='*')
async def edit_experience_retrieve_menu(call: types.CallbackQuery,
                                        state: FSMContext) -> None:
    await state.finish()

    retrieve_exp = await UserExperience.get(
        EditExperienceKeyboard.parse_experience_id(call.data),
    )
    await call.message.edit_text(
        get_experience_retrieve_text(retrieve_exp),
        reply_markup=EditExperienceRetrieveKeyboard.get_keyboard(
            retrieve_exp.id,
        ),
    )


@dp.callback_query_handler(
    text_startswith=EditExperienceRetrieveKeyboard.call_prefix)
async def ask_new_value(call: types.CallbackQuery, state: FSMContext) -> None:
    field_name, exp_id = EditExperienceRetrieveKeyboard.parse_call_data(
        call.data,
    )
    await state.update_data(field_name=field_name, exp_id=exp_id)
    await call.message.edit_text(
        'Пришлите новое значения для поля',
        reply_markup=BackToEditExperienceRetrieveKeyboard.get_keyboard(exp_id),
    )
    await ExperienceRetrieveState.value.set()


@dp.message_handler(state=ExperienceRetrieveState.value)
async def get_and_edit_value(message: types.Message,
                             state: FSMContext) -> None:
    data = await state.get_data()
    await state.finish()

    exp_id = data.get('exp_id')
    await UserExperience.update(
        exp_id=exp_id,
        **{data.get('field_name'): message.text},
    )

    await message.answer(
        'Поле успешно изменено',
        reply_markup=BackToEditExperienceRetrieveKeyboard.get_keyboard(exp_id),
    )
