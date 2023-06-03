from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.projects import BACK_TO_PROJECTS_CALL


class ProjectsKeyboard:
    create_project_call = 'projects_create'
    my_projects_call = 'projects_my'
    project_notice_call = 'projects_notice'
    match_project_call = 'projects_match'

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                'Создать проект',
                callback_data=create_project_call,
            ),
            InlineKeyboardButton(
                'Мои проекты',
                callback_data=my_projects_call,
            ),
        ],
        [
            InlineKeyboardButton(
                'Уведомления',
                callback_data=project_notice_call
            ),
        ],
        [
            InlineKeyboardButton(
                'Проект матчинг',
                callback_data=match_project_call,
            ),
        ],
    ])


class BackToCreateProjectKeyboard:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            'Вернуться назад',
            callback_data=ProjectsKeyboard.create_project_call,
        ),
    ]])


class BackToMainProjectsKeyboard:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            'Вернуться к проектам',
            callback_data=BACK_TO_PROJECTS_CALL,
        ),
    ]])
