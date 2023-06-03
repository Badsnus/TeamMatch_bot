from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.projects import MyProjectRetrieveKeyboard, \
    MyProjectCandidatesKeyboard
from loader import dp
from models import Project


@dp.callback_query_handler(
    text_startswith=MyProjectRetrieveKeyboard.edit_cand_call)
async def show_candidates_menu(call: types.CallbackQuery,
                               state: FSMContext) -> None:
    project_id = MyProjectRetrieveKeyboard.parse_project_id(call.data)
    await state.update_data(project_id=project_id)

    project = await Project.get(project_id, do_join=True)

    await call.message.edit_text(
        'Выберите вакансию для изменения',
        reply_markup=MyProjectCandidatesKeyboard.get_keyboard(
            project.candidates,
        ),
    )
