from data.config import BOT_URL_FOR_REF
from keyboards.inline.projects import CreateProjectKeyboard
from models import Project


def get_projects_main_menu_text() -> str:
    return 'Проекты'


def get_field_symbol(field: str,
                     good_value: str = '✅',
                     bad_value: str = '❌') -> str:
    return good_value if field else bad_value


def format_field_text(field: str, value: str) -> str:
    return f'<b>{field}</b>: <code>{value}</code>'


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
{format_field_text('Ссылка на проект <code>(Необязательно)</code>', project_url)}

{format_field_text('Логотип', logo_image_id)}
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


def get_project_retrieve_text(project: Project) -> str:
    employees_text = '\n'.join(
        f'<a href="{BOT_URL_FOR_REF}{employee.user_id}">'
        f'{employee.user.name}</a> - <code>{employee.role}</code>'
        for employee in project.employees
    )
    candidates_text = '\n.'.join(
        f'<b>{index}.</b><code>{candidate.role}</code>'
        for index, candidate in enumerate(project.candidates, start=1)
    ) if project.candidates else '<code>Вакансий нет.</code>'

    return f'''
{format_field_text('Название', project.name)}   

{format_field_text('Описание', project.description)}
{format_field_text('Ссылка на проект', project.project_url)}

{format_field_text('Показывается для метчинга',
                   get_field_symbol(project.show_for_matching))}
                   
<b>Сотрудники:</b>\n{employees_text}\n
<b>Нужны сотрудники:</b>\n{candidates_text}\n
    '''
