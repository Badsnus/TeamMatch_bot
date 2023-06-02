from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.profile import EditExperienceKeyboard
from loader import dp
from models import User, UserExperience
from services.profile import get_experience_retrieve_text


@dp.callback_query_handler(
    text_startswith=EditExperienceKeyboard.edit_call_prefix)
async def edit_experience_retrieve_menu(call: types.CallbackQuery,
                                        user: User,
                                        state: FSMContext) -> None:
    await state.finish()

    retrieve_exp = await UserExperience.get(
        EditExperienceKeyboard.parse_experience_id(call.data),
    )
    await call.message.edit_text(
        get_experience_retrieve_text(retrieve_exp),
    )
