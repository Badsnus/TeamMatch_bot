from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import Vacancy


class VacanciesSliderKeyboard:
    slider_callback = 'vacancy_slider-'
    slider_right = slider_callback + 'right-'
    slider_left = slider_callback + 'left-'

    @staticmethod
    def generate_callback(current_callback: str, vacancy_id: int) -> str:
        return current_callback + str(vacancy_id)

    @classmethod
    def get_keyboard(cls, vacancy: Vacancy) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    'Откликнуться',
                    url=vacancy.url_for_response,
                ),
            ],
            [
                InlineKeyboardButton(
                    '🔙',
                    callback_data=cls.generate_callback(
                        cls.slider_left,
                        vacancy.id,
                    ),
                ),
                InlineKeyboardButton(
                    '🔜',
                    callback_data=cls.generate_callback(
                        cls.slider_right,
                        vacancy.id,
                    ),
                ),
            ],
        ])
        return keyboard
