from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import BACK_TO_MY_PROJECT_RETRIEVE
from models import Candidate


class MyProjectCandidatesKeyboard:
    edit_candidate_call = 'my_projects_candidates_edit-'
    add_candidate_call = 'my_projects_candidates_add'

    @classmethod
    def parse_employee_id(cls, call_data: str) -> int:
        return int(call_data.replace(cls.edit_candidate_call, ''))

    @classmethod
    def get_call_data(cls, candidate_id: int) -> str:
        return f'{cls.edit_candidate_call}{candidate_id}'

    @classmethod
    def get_keyboard(cls, candidates: list[Candidate]) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        for candidate in candidates:
            keyboard.insert(
                InlineKeyboardButton(
                    candidate.role,
                    callback_data=cls.get_call_data(candidate.id),
                ),
            )
        keyboard.row(InlineKeyboardButton(
            'Добавить вакансию',
            callback_data=cls.add_candidate_call,
        ))
        keyboard.row(InlineKeyboardButton(
            'Вернуться назад',
            callback_data=BACK_TO_MY_PROJECT_RETRIEVE,
        ))

        return keyboard

    # TODO удалить
    @classmethod
    def get_back_keyboard(cls, candidate_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                'Назад',
                callback_data=cls.get_call_data(candidate_id),
            ),
        ]])
