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
    employee = await Candidate.get(candidate_id)

    await state.update_data(candidate_id=candidate_id)

    await call.message.edit_text(
        get_candidate_text(employee),
        reply_markup=ProjectCandidateRetrieveKeyboard.get_keyboard(
            employee.project_id,
        ),
    )
