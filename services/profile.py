from models import User, UserContact, UserExperience, UserSkill
from services.projects import get_link_to_user
from utils.format_data import format_username


def get_experience_text(experience: list[UserExperience]) -> str:
    experience_text = '\n'.join(
        f'<code>{exp.name}</code> - <a href="{exp.link}">ссылка</a>'
        for exp in experience
    )
    if not experience_text:
        experience_text = '<code>Опыта пока что нет нет :(</code>'
    return '\n\n<b>Ваш опыт:</b>\n' + experience_text


def get_current_skills_text(skills: list[UserSkill]) -> str:
    skills_text = ';'.join(skill.name for skill in skills)
    if not skills_text:
        skills_text = 'Скиллов пока что нет нет :('
    return '\n\n<b>Ваши скиллы:</b>\n<code>' + skills_text + '</code>'


def get_profile_text(user: User) -> str:
    contacts_text = '\n\n<b>Ваши контакты:</b>\n' + '\n'.join(
        (f'<code>{contact.name}</code> - {contact.link}' for contact in
         user.contacts),
    ) if user.contacts else ''
    skills_text = get_current_skills_text(user.skills) if user.skills else ''
    experience_text = (
        get_experience_text(user.experience) if user.experience else ''
    )
    date_of_reg = user.registration_time.date()

    return (
            f'''
<b>Профиль</b> | ID: <code>{user.id}</code>

<b>Имя:</b> {get_link_to_user(user.id, user.name)}
<b>Юзернейм:</b> {format_username(user.telegram_username)}
<b>Дата регистрации::</b> <code>{date_of_reg}</code>''' +
            f'{contacts_text}{skills_text}{experience_text}'
    )


def get_contact_text(contact: UserContact) -> str:
    return f'''
<b>Имя:</b> <code>{contact.name}</code>
<b>Ссылка:</b> <code>{contact.link}</code>
    '''


def get_experience_retrieve_text(experience: UserExperience) -> str:
    return f'''
<b>Название</b>: <code>{experience.name}</code>
<b>Ссылка</b>: <code>{experience.link}</code>
<b>Описание</b>: <code>{experience.description}</code>
    '''


class SkillsAppender:

    @staticmethod
    def get_ask_text() -> str:
        return ('Пришлите скилы, каждый скилл в новой строке\n'
                'Например:<code>\n'
                'Pyhon\n'
                'Django\n'
                'Js</code>')

    @staticmethod
    def parse_skills(row_skills: str) -> list[str]:
        return row_skills.split('\n')

    @classmethod
    async def create_skills(cls,
                            row_skills: str,
                            user_id: int) -> list[UserSkill]:
        skills = cls.parse_skills(row_skills)

        return await UserSkill.create_many(user_id, skills)
