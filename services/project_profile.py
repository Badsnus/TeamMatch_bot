from models import Project
from services.projects import (
    get_employees_and_candidate_text,
    format_field_text,
)


def get_project_profile_text(project: Project) -> str:
    employees_text, candidates_text = get_employees_and_candidate_text(project)
    return f'''
{format_field_text('Название', project.name)}   

{format_field_text('Описание', project.description)}
{format_field_text('Ссылка на проект', project.project_url)}

<b>Сотрудники:</b>\n{employees_text}\n
<b>Текущие вакансии:</b>\n{candidates_text}\n
        '''
