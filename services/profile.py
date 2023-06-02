from models import User, UserContact, UserExperience, UserSkill
from utils.format_data import format_date_from_timestamp, format_username


def get_experience_text(experience: list[UserExperience]) -> str:
    experience_text = '\n'.join(
        f'<code>{exp.name}</code> - <a href="{exp.link}">ссылка</a>\n'
        for exp in experience
    )
    if not experience_text:
        experience_text = '<code>Опыта пока что нет нет :(</code>'
    return '\nВаш опыт:\n' + experience_text


def get_current_skills_text(skills: list[UserSkill]) -> str:
    skills_text = ';'.join(skill.name for skill in skills)
    if not skills_text:
        skills_text = 'Скиллов пока что нет нет :('
    return '\nВаши скиллы:\n<code>' + skills_text + '</code>'


def get_profile_text(user: User) -> str:
    contacts_text = '\nВаши контакты:\n' + '\n'.join(
        (f'<code>{contact.name}</code> - {contact.link}' for contact in
         user.contacts),
    ) if user.contacts else ''
    skills_text = get_current_skills_text(user.skills) if user.skills else ''
    experience_text = (
        get_experience_text(user.experience) if user.experience else ''
    )

    return f'''
Профиль | {user.telegram_id}

Имя: {user.name}
Юзернейм: {format_username(user.telegram_username)}
Дата регистрации: {format_date_from_timestamp(user.registration_time)}
{contacts_text}
{skills_text}
{experience_text}
    '''


def get_contact_text(contact: UserContact) -> str:
    return f'''
Имя: <code>{contact.name}</code>
Ссылка: {contact.link}
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
