from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.profile import ProfileKeyboard, BackToProfileKeyboard
from loader import dp
from models import User
from states.profile import EditNameState


@dp.callback_query_handler(text=ProfileKeyboard.change_name)
async def ask_new_name(call: types.CallbackQuery) -> None:
    await call.message.edit_text(
        "Введите новое имя",
        reply_markup=BackToProfileKeyboard.keyboard,
    )
    await EditNameState.name.set()


@dp.message_handler(state=EditNameState.name)
async def change_name(message: types.Message,
                      user: User,
                      state: FSMContext) -> None:
    await state.finish()
    await user.update(name=message.text)
    await message.answer(
        f'Ваше имя изменено на {message.text}',
        reply_markup=BackToProfileKeyboard.keyboard,
    )
