from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import BACK_TO_PROJECTS_CALL


class MatchKeyboard:
    give_info_call = 'match_give_info-'
    next_project_call = 'match_next_project-'

    @staticmethod
    def parse_project_id(call_data: str) -> int:
        _, project_id = call_data.split('-')
        return int(project_id)

    @staticmethod
    def get_call_data(prefix: str, project_id: int) -> str:
        return prefix + str(project_id)

    @classmethod
    def get_keyboard(cls, project_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Оставить мне информацию про проект',
                    callback_data=cls.get_call_data(
                        cls.give_info_call,
                        project_id,
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Выйти',
                    callback_data=BACK_TO_PROJECTS_CALL,
                ),
                InlineKeyboardButton(
                    text='Некст проект',
                    callback_data=cls.get_call_data(
                        cls.next_project_call,
                        project_id,
                    ),
                ),
            ],
        ])
