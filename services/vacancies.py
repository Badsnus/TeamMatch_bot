from models import Vacancy


def get_vacancy_text(vacancy: Vacancy) -> str:
    return f'''
<b>{vacancy.title}</b>

<i>{vacancy.description}</i>
    '''
