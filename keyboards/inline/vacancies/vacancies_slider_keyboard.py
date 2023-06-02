from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import Vacancy


class VacanciesSliderKeyboard:
    RIGHT = 'right'
    LEFT = 'left'

    slider_callback = 'vacancy_slider-'
    slider_right = slider_callback + RIGHT
    slider_left = slider_callback + LEFT

    @classmethod
    def parse_callback(cls, callback: str) -> tuple[str, int]:
        _, direction, vacancy_id = callback.split('-')
        return direction, int(vacancy_id)

    @staticmethod
    def generate_callback(current_callback: str, vacancy_id: int) -> str:
        return f'{current_callback}-{vacancy_id}'

    @staticmethod
    def _add_button(buttons: list[InlineKeyboardButton],
                    statement: bool,
                    button_text: str,
                    button_callback: str,
                    ) -> list[InlineKeyboardButton]:
        if statement:
            buttons.append(
                InlineKeyboardButton(
                    button_text,
                    callback_data=button_callback,
                ),
            )
        return buttons

    @classmethod
    def get_keyboard(cls,
                     vacancy: Vacancy,
                     need_left: bool,
                     need_right: bool,
                     ) -> InlineKeyboardMarkup:
        scroll_buttons = []

        cls._add_button(
            scroll_buttons,
            need_left,
            '🔙',
            cls.generate_callback(cls.slider_left, vacancy.id),
        )
        cls._add_button(
            scroll_buttons,
            need_right,
            '🔜',
            cls.generate_callback(cls.slider_right, vacancy.id),
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    'Откликнуться',
                    url=vacancy.url_for_response,
                ),
            ],
            scroll_buttons,
        ])
        return keyboard
