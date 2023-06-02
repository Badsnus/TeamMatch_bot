from keyboards.inline.vacancies import VacanciesSliderKeyboard
from models import Vacancy
from utils.exceptions import DoNotFindVacancyForSlider


def get_vacancy_text(vacancy: Vacancy) -> str:
    return f'''
<b>{vacancy.title}</b>

<i>{vacancy.description}</i>
    '''


def check_need_direction(vacancy_count: int) -> bool:
    # if we dont have second vacancy after it we should set need_*=False
    # cuz its last vacancy
    return vacancy_count == 2


async def get_vacancy_and_offset(direction: str,
                                 vacancy_id: int,
                                 need_left=True,
                                 need_right=True,
                                 ) -> tuple[Vacancy, bool, bool]:
    vacancies = await Vacancy.get_queryset_by_filters(
        Vacancy.id < vacancy_id if direction == VacanciesSliderKeyboard.RIGHT
        else Vacancy.id > vacancy_id,
        use_desc=True,
    )

    if not vacancies:
        raise DoNotFindVacancyForSlider

    if direction == VacanciesSliderKeyboard.RIGHT:
        need_right = check_need_direction(len(vacancies))
        vacancy = vacancies[0]
    else:
        need_left = check_need_direction(len(vacancies))
        vacancy = vacancies[need_left]  # cuz len(vacancies) can be 1

    return vacancy, need_left, need_right


async def get_vacancy_start_index() -> int:
    vacancies = await Vacancy.get_queryset_by_filters(use_desc=True, limit=1)

    if not vacancies:
        raise DoNotFindVacancyForSlider

    return vacancies[0].id + 1  # cuz we need to take this vacancy
