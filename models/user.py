from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, ForeignKey, orm, select, String

from models.base_model import Base
from models.exceptions import (
    UserContactNotFound,
    UserExperienceNotFound,
    UserSkillNotFound,
)
from loader import session


# TODO эт бы по файлам разнести
# TODO мб подумать про repeat кода в create(), update() и т.д.
class User(Base):
    __tablename__ = 'user'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    telegram_id: orm.Mapped[int] = orm.mapped_column(
        Integer(),
        index=True,
        unique=True,
    )
    name: orm.Mapped[str] = orm.mapped_column(
        String(40),
    )
    telegram_username: orm.Mapped[str | None] = orm.mapped_column(
        String(40),
        nullable=True,
    )
    # TODO это мб в редис вынести куда-то? чтобы бд не дергать постоянно
    last_active: orm.Mapped[int] = orm.mapped_column(
        DateTime(),
    )
    registration_time: orm.Mapped[int] = orm.mapped_column(
        DateTime(),
    )

    contacts: orm.Mapped[list['UserContact']] = orm.relationship(
        back_populates='user', cascade='all, delete-orphan',
    )
    skills: orm.Mapped[list['UserSkill']] = orm.relationship(
        back_populates='user', cascade='all, delete-orphan',
    )
    experience: orm.Mapped[list['UserExperience']] = orm.relationship(
        back_populates='user', cascade='all, delete-orphan',
    )

    projects: orm.Mapped[list['Project']] = orm.relationship(
        secondary='employee', back_populates='users',
    )
    employees: orm.Mapped[list['Employee']] = orm.relationship(
        back_populates='user',
    )
    invites_to_employee: orm.Mapped[list['InviteToEmployee']] = (
        orm.relationship(
            back_populates='user',
            cascade='all, delete-orphan',
        )
    )

    @staticmethod
    async def get(user_id: int) -> User:
        user = await session.scalar(
            select(User).where(User.id == user_id).limit(1),
        )

        if user is None:
            raise Exception  # TODO need exp

        return user

    @staticmethod
    async def get_user_with_projects(user_id: int) -> User:
        from models import Employee, Project  # circ import

        user = await session.scalar(
            select(User)
            .where(User.id == user_id)
            .outerjoin(Employee, Employee.user_id == user_id)
            .outerjoin(Project, Employee.project_id == Project.id)
            .outerjoin(UserContact)
            .outerjoin(UserSkill)
            .outerjoin(UserExperience)
            .options(orm.selectinload(User.projects))
            .options(orm.selectinload(User.contacts))
            .options(orm.selectinload(User.skills))
            .options(orm.selectinload(User.experience))
            .limit(1),
        )

        if user is None:
            raise Exception  # TODO need exp

        return user

    @staticmethod
    async def get_by_telegram_id(telegram_id: int) -> User | None:
        # TODO оптимизация запросов
        return await session.scalar(
            select(User).where(User.telegram_id == telegram_id)
            .outerjoin(UserContact)
            .outerjoin(UserSkill)
            .outerjoin(UserExperience)
            .options(orm.selectinload(User.contacts))
            .options(orm.selectinload(User.skills))
            .options(orm.selectinload(User.experience))
        )

    @staticmethod
    async def create(telegram_id: int, name: str,
                     telegram_username: str | None = None) -> User:
        user = User(
            telegram_id=telegram_id,
            name=name,
            telegram_username=telegram_username,
            last_active=datetime.now(),
            registration_time=datetime.now(),
        )

        session.add(user)
        await session.commit()

        return user

    async def update(self, commit=True, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if commit:
            await session.commit()

    async def refresh(self):
        await session.refresh(self)


# TODO ограничить число контактов
class UserContact(Base):
    __tablename__ = 'user_contact'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    user_id: orm.Mapped[int] = orm.mapped_column(ForeignKey('user.id'))
    user: orm.Mapped[User] = orm.relationship(back_populates='contacts')

    name: orm.Mapped[str] = orm.mapped_column(String(30))
    link: orm.Mapped[str] = orm.mapped_column(String(60))

    @staticmethod
    async def create(user_id: int, name: str, link: str) -> UserContact:
        contact = UserContact(
            user_id=user_id,
            name=name,
            link=link,
        )

        session.add(contact)
        await session.commit()

        return contact

    @staticmethod
    async def update(contact_id: int, **kwargs) -> UserContact:
        contact = await UserContact.get(contact_id)
        for key, value in kwargs.items():
            setattr(contact, key, value)

        await session.commit()

        return contact

    @staticmethod
    async def get(contact_id: int) -> UserContact:
        contact = await session.scalar(
            select(UserContact).where(UserContact.id == contact_id).limit(1),
        )

        if contact is None:
            raise UserContactNotFound

        return contact

    @staticmethod
    async def delete(contact_id: int) -> None:
        await session.delete(await UserContact.get(contact_id))
        await session.commit()


# TODO сюда тоже надо ограничение на количество
class UserSkill(Base):
    __tablename__ = 'user_skill'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    user_id: orm.Mapped[int] = orm.mapped_column(ForeignKey('user.id'))
    user: orm.Mapped[User] = orm.relationship(back_populates='skills')

    name: orm.Mapped[str] = orm.mapped_column(String(50))

    @staticmethod
    async def create_many(user_id: int,
                          skills_list: list[str]) -> list[UserSkill]:
        user_skills = [
            UserSkill(user_id=user_id, name=skill)
            for skill in skills_list
        ]

        session.add_all(user_skills)
        await session.commit()

        return user_skills

    @staticmethod
    async def get(skill_id: int) -> UserSkill:
        skill = await session.scalar(
            select(UserSkill).where(UserSkill.id == skill_id).limit(1),
        )

        if skill is None:
            raise UserSkillNotFound

        return skill

    @staticmethod
    async def delete(skill_id: int) -> None:
        await session.delete(await UserSkill.get(skill_id))
        await session.commit()


class UserExperience(Base):
    __tablename__ = 'user_experience'
    # Костыльный вариант на время мвп, потом надо добавить дату и пр.
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    name: orm.Mapped[str] = orm.mapped_column(String(50))
    link: orm.Mapped[str] = orm.mapped_column(String(60))
    description: orm.Mapped[str] = orm.mapped_column(String(300))

    user_id: orm.Mapped[int] = orm.mapped_column(ForeignKey('user.id'))
    user: orm.Mapped[User] = orm.relationship(back_populates='experience')

    @staticmethod
    async def create(user_id: int,
                     name: str,
                     link: str,
                     description: str) -> UserExperience:
        experience = UserExperience(
            user_id=user_id,
            name=name,
            link=link,
            description=description,
        )

        session.add(experience)
        await session.commit()

        return experience

    @staticmethod
    async def get(experience_id: int) -> UserExperience:
        experience = await session.scalar(
            select(UserExperience).where(UserExperience.id == experience_id)
            .limit(1),
        )

        if experience is None:
            raise UserExperienceNotFound

        return experience

    @staticmethod
    async def update(exp_id: int, **kwargs) -> UserExperience:
        experience = await UserExperience.get(exp_id)
        for key, value in kwargs.items():
            setattr(experience, key, value)

        await session.commit()

        return experience

    @staticmethod
    async def delete(exp_id: int) -> None:
        await session.delete(await UserExperience.get(exp_id))
        await session.commit()
