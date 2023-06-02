from aiogram.dispatcher.filters.state import State, StatesGroup

from models import UserExperience


class AddExperienceState(StatesGroup):
    name = State()
    link = State()
    description = State()

    UETC = UserExperience.__table__.c

    name_text = (
        '<b>Введите название компании/проекта\n</b><code>'
        f'Имя не должно превышать {UETC.name.type.length} символов</code>'
    )
    link_text = (
        '<b>Введите ссылку на компанию/проект\n</b><code>'
        f'Ссылка не должна превышать {UETC.link.type.length} символов</code>'
    )
    description_text = (
        '<b>Напишите краткое описание того, чем вы '
        'занимались на этом проекте\n</b><code>Описание не должно '
        f'превышать {UETC.description.type.length} символов</code>'
    )
