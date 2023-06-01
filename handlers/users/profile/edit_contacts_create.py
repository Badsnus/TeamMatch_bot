from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.exc import DataError

from keyboards.inline.profile import (
    BackToEditContactsMenu,
    EditContactsKeyboard,
)
from loader import dp
from models import User, UserContact
from states.profile import CreateContactState


@dp.callback_query_handler(text=EditContactsKeyboard.callback_create_prefix)
async def start_create_contact(call: types.CallbackQuery) -> None:
    await call.message.edit_text(
        'Пришлите название контакта',
        reply_markup=BackToEditContactsMenu.keyboard,
    )
    await CreateContactState.name.set()


@dp.message_handler(state=CreateContactState.name)
async def get_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data({CreateContactState.name_field_name: message.text})
    await message.answer(
        'Пришлите ссылку, на который этот контакт будет ввести',
        reply_markup=BackToEditContactsMenu.keyboard,
    )
    await CreateContactState.link.set()


@dp.message_handler(state=CreateContactState.link)
async def create_contact(message: types.Message, state: FSMContext,
                         user: User) -> None:
    data = await state.get_data()
    await state.finish()

    name = data.get(CreateContactState.name_field_name)
    link = message.text
    try:
        contact = await UserContact.create(user.id, name, link)
        text = f'Контакт <code>{contact.name}</code> - успешно создан'

    except DataError as _:
        name_limit = UserContact.__table__.c.name.type.length
        link_limit = UserContact.__table__.c.link.type.length
        text = (
            'Вы превысили ограничения для контакта:\n'
            f'Название контакта не более {name_limit} символов\n'
            f'Ссылка на контакт не более {link_limit} символов'
        )

    await message.answer(
        text,
        reply_markup=BackToEditContactsMenu.keyboard,
    )
