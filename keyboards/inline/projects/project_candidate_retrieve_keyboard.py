from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import MyProjectRetrieveKeyboard


class ProjectCandidateRetrieveKeyboard:
    edit_role_call = 'project_candidate_retrieve_edit_role'
    edit_desc_call = 'project_candidate_retrieve_edit_desc'
    delete_call = 'project_candidate_retrieve_delete'

    @classmethod
    def get_keyboard(cls, project_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Редактировать роль',
                    callback_data=cls.edit_role_call
                ),
                InlineKeyboardButton(
                    text='Редактировать описание',
                    callback_data=cls.edit_role_call
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Удалить вакансию',
                    callback_data=cls.delete_call,
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Вернуться ко всем вакансиям',
                    callback_data=MyProjectRetrieveKeyboard.generate_call_data(
                        MyProjectRetrieveKeyboard.edit_cand_call, project_id,
                    ),
                ),
            ],
        ])
