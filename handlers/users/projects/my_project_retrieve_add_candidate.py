from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.projects import (
    BackToCandidateKeyboard,
    MyProjectCandidatesKeyboard,
)
from loader import dp
from models import Candidate
from states.projects import AddCandidateState

# TODO это мне стало совсем лень, надо бы разбить логику
SPLIT_BY = ';'


@dp.callback_query_handler(text=MyProjectCandidatesKeyboard.add_candidate_call)
async def ask_data(call: types.CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    project_id = data.get('project_id')

    await call.message.edit_text(
        f'Введите роль вакансии и описание требований через {SPLIT_BY}\n'
        f'Например: <code>backend{SPLIT_BY}нужно делать Api</code>',
        reply_markup=BackToCandidateKeyboard.get_keyboard(project_id),
    )
    await AddCandidateState.value.set()


@dp.message_handler(state=AddCandidateState.value)
async def add_candidate(message: types.Message, state: FSMContext) -> None:
    await state.reset_state(with_data=False)
    data = await state.get_data()

    project_id = data.get('project_id')

    if message.text.count(SPLIT_BY) != 1:
        await message.answer(
            '<code>Я тебя не понял :(</code>',
            reply_markup=BackToCandidateKeyboard.get_keyboard(project_id),
        )
        return
    role, description = message.text.split(SPLIT_BY)
    candidate = Candidate(
        description=description,
        project_id=project_id,
        role=role,
    )
    await candidate.save()

    await message.answer(
        '<b>Вакансия добавлена</b>',
        reply_markup=BackToCandidateKeyboard.get_keyboard(project_id),
    )
