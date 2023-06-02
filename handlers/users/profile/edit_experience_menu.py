from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.profile import EditExperienceKeyboard, ProfileKeyboard
from loader import dp
from models import User
from services.profile import get_experience_text


@dp.callback_query_handler(text=ProfileKeyboard.change_experience, state='*')
async def show_edit_experience_menu(call: types.CallbackQuery,
                                    user: User,
                                    state: FSMContext) -> None:
    await state.finish()

    await call.message.edit_text(
        text=get_experience_text(user.experience),
        reply_markup=EditExperienceKeyboard.get_keyboard(user.experience),
    )
