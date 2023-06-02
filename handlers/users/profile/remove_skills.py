from aiogram import types

from keyboards.inline.profile import EditSkillsKeyboard, DeleteSkillKeyboard
from loader import dp
from models import User, UserSkill


@dp.callback_query_handler(text=EditSkillsKeyboard.delete_skills_menu)
async def show_delete_skills_menu(call: types.CallbackQuery,
                                  user: User) -> None:
    await call.message.edit_text(
        text=DeleteSkillKeyboard.TEXT,
        reply_markup=DeleteSkillKeyboard.get_keyboard(user.skills),
    )


@dp.callback_query_handler(
    text_startswith=DeleteSkillKeyboard.delete_skill_call)
async def delete_skill(call: types.CallbackQuery, user: User) -> None:
    skill_id = DeleteSkillKeyboard.parse_skill_id_by_callback(
        call.data,
    )
    await UserSkill.delete(skill_id)
    await user.refresh()

    await call.answer('Скилл удален')

    await call.message.edit_text(
        text=DeleteSkillKeyboard.TEXT,
        reply_markup=DeleteSkillKeyboard.get_keyboard(user.skills),
    )
