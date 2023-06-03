from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.projects import (
    MyProjectCandidatesKeyboard,
    MyProjectRetrieveKeyboard,
    ProjectCandidateRetrieveKeyboard,
)
from loader import dp
from models import Candidate, Project
from services.projects import get_candidate_text
from states.projects import UpdateCandidateDataState


@dp.callback_query_handler(
    text_startswith=MyProjectRetrieveKeyboard.edit_cand_call, state='*')
async def show_candidates_menu(call: types.CallbackQuery,
                               state: FSMContext) -> None:
    await state.finish()

    project_id = MyProjectRetrieveKeyboard.parse_project_id(call.data)
    await state.update_data(project_id=project_id)

    project = await Project.get(project_id, do_join=True)

    await call.message.edit_text(
        'Выберите вакансию для изменения',
        reply_markup=MyProjectCandidatesKeyboard.get_keyboard(
            project.candidates,
        ),
    )


@dp.callback_query_handler(
    text_startswith=MyProjectCandidatesKeyboard.edit_candidate_call, state='*')
async def show_employee_retrieve_menu(call: types.CallbackQuery,
                                      state: FSMContext) -> None:
    await state.reset_state(with_data=False)

    candidate_id = MyProjectCandidatesKeyboard.parse_candidate_id(call.data)
    candidate = await Candidate.get(candidate_id)

    await state.update_data(candidate_id=candidate_id)

    await call.message.edit_text(
        get_candidate_text(candidate),
        reply_markup=ProjectCandidateRetrieveKeyboard.get_keyboard(
            candidate.project_id,
        ),
    )


@dp.callback_query_handler(
    text_startswith=ProjectCandidateRetrieveKeyboard.edit_prefix)
async def ask_new_role(call: types.CallbackQuery, state: FSMContext) -> None:
    field_name = ProjectCandidateRetrieveKeyboard.parse_field_name(call.data)
    text_field = ProjectCandidateRetrieveKeyboard.text_for_fields[field_name]

    await state.update_data(field_name=field_name)

    data = await state.get_data()
    candidate_id = data.get('candidate_id')

    await call.message.edit_text(
        text_field,
        reply_markup=MyProjectCandidatesKeyboard.get_back_keyboard(
            candidate_id,
        ),
    )

    await UpdateCandidateDataState.value.set()


@dp.message_handler(state=UpdateCandidateDataState.value)
async def update_role(message: types.Message, state: FSMContext) -> None:
    await state.reset_state(with_data=False)
    data = await state.get_data()

    candidate_id = data.get('candidate_id')
    field_name = data.get('field_name')

    candidate = await Candidate.get(candidate_id)
    await candidate.update(**{field_name: message.text})

    await message.answer(
        get_candidate_text(candidate),
        reply_markup=ProjectCandidateRetrieveKeyboard.get_keyboard(
            candidate.project_id,
        ),
    )
