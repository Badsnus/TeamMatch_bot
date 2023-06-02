from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.profile import (
    BackToEditExperienceKeyboard,
    EditExperienceKeyboard,
)
from loader import dp
from models import User, UserExperience
from states.profile import AddExperienceState


@dp.callback_query_handler(text=EditExperienceKeyboard.add_call)
async def ask_name(call: types.CallbackQuery) -> None:
    await AddExperienceState.name.set()

    await call.message.edit_text(
        AddExperienceState.name_text,
        reply_markup=BackToEditExperienceKeyboard.keyboard,
    )


@dp.message_handler(state=AddExperienceState.name)
async def ask_link(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await AddExperienceState.link.set()

    await message.answer(
        AddExperienceState.link_text,
        reply_markup=BackToEditExperienceKeyboard.keyboard,
    )


@dp.message_handler(state=AddExperienceState.link)
async def ask_description(message: types.Message, state: FSMContext) -> None:
    await state.update_data(link=message.text)
    await AddExperienceState.description.set()

    await message.answer(
        AddExperienceState.description_text,
        reply_markup=BackToEditExperienceKeyboard.keyboard,
    )


@dp.message_handler(state=AddExperienceState.description)
async def get_description_and_create_experience(message: types.Message,
                                                user: User,
                                                state: FSMContext) -> None:
    data = await state.get_data()
    await state.finish()

    await UserExperience.create(
        user_id=user.id,
        name=data.get('name'),
        link=data.get('link'),
        description=message.text,
    )

    await message.answer(
        '<b>Опыт работы создан</b>',
        reply_markup=BackToEditExperienceKeyboard.keyboard,
    )
