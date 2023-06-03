from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import MyProjectRetrieveKeyboard
from models import Candidate


class ProjectCandidateRetrieveKeyboard:
    text_for_fields = {
        Candidate.role.key: 'Введите новую роль',
        Candidate.description.key: 'Введите новое описание',
    }

    edit_prefix = 'project_candidate_retrieve_edit_'
    edit_role_call = edit_prefix + Candidate.role.key
    edit_desc_call = edit_prefix + Candidate.description.key
    delete_call = 'project_candidate_retrieve_delete'

    @classmethod
    def parse_field_name(cls, callback_data: str) -> str:
        return callback_data.replace(cls.edit_prefix, '')

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
                    callback_data=cls.edit_desc_call
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
