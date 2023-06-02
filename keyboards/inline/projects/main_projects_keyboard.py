from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class ProjectKeyboard:
    create_project_call = 'projects_create_project'
    my_projects_call = 'projects_my_projects'
    project_notice_call = 'projects_notice'
    match_project_call = 'projects_match'

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                'Создать проект',
                callback_data=create_project_call,
            ),
            InlineKeyboardButton(
                'Редактировать проекты',
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
