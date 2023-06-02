from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.profile import EditSkillsKeyboard, ProfileKeyboard
from loader import dp
from models import User
from services.profile import get_current_skills_text


@dp.callback_query_handler(text=ProfileKeyboard.change_skills, state='*')
async def show_edit_skills_menu(call: types.CallbackQuery,
                                user: User,
                                state: FSMContext) -> None:
    await state.finish()

    await call.message.edit_text(
        text=get_current_skills_text(user.skills),
        reply_markup=EditSkillsKeyboard.keyboard,
    )
