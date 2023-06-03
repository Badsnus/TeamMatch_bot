from keyboards.inline.projects import CreateProjectKeyboard


class MyProjectEditSettingsKeyboard(CreateProjectKeyboard):
    create_text = 'Сохранить изменения'
    approve_create_call = 'project_my_settings_approve_change'

    back_text = 'Вернуться к настройкам проекта'
    back_call = 'project_my_settings_back'
