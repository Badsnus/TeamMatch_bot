from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.profile import (
    BackToEditSkillsKeyboard,
    EditSkillsKeyboard,
)
from loader import dp
from models import User
from services.profile import SkillsAppender
from states.profile import AddSkillsState


@dp.callback_query_handler(text=EditSkillsKeyboard.add_skill_call)
async def ask_skills(call: types.CallbackQuery, state: FSMContext):
    await AddSkillsState.skills.set()

    await call.message.edit_text(
        SkillsAppender.get_ask_text(),
        reply_markup=BackToEditSkillsKeyboard.keyboard,
    )


@dp.message_handler(state=AddSkillsState.skills)
async def add_skills(message: types.Message,
                     user: User,
                     state: FSMContext) -> None:
    await state.finish()

    await SkillsAppender.create_skills(message.text, user.id)

    await message.answer(
        'Скиллы добавлены',
        reply_markup=BackToEditSkillsKeyboard.keyboard,
    )
