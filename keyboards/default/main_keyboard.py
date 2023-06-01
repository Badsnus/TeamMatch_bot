from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class MainKeyboard:
    projects = 'Проекты'
    vacancies = 'Вакансии и стажировки'
    profile = 'Профиль'

    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(projects),
                KeyboardButton(vacancies),
            ],
            [
                KeyboardButton(profile)
            ],
        ],
    )
