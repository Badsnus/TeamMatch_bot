from keyboards.inline.projects import CreateProjectKeyboard


def get_projects_main_menu_text() -> str:
    return 'Проекты'


def get_field_symbol(field: str,
                     good_value: str = '✅',
                     bad_value: str = '❌') -> str:
    return good_value if field else bad_value


def format_field_text(field: str, value: str) -> str:
    return f'<b>{field}</b>: <code>{value}</code>\n'


def get_create_project_text(
        name: str,
        description: str,
        logo_image_id: str,
        project_url: str) -> str:
    name = get_field_symbol(name, name)
    description = get_field_symbol(description, description)
    logo_image_id = get_field_symbol(logo_image_id)
    project_url = get_field_symbol(project_url, project_url)
    return f'''
{format_field_text('Название', name)}
{format_field_text('Описание', description)}
{format_field_text('Логотип', logo_image_id)}
{format_field_text('Ссылка на проект <code>(Необязательно)</code>', project_url)}
    '''


def get_fields_values(data: dict) -> list[str]:
    return [
        data.get(field.value, '') for field in CreateProjectKeyboard.Fields
    ]


def get_fields_items(data: dict) -> dict[str, str]:
    return dict(zip(
        (field.value for field in CreateProjectKeyboard.Fields),
        get_fields_values(data),
    ))
