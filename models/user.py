from __future__ import annotations

import time

from sqlalchemy import Integer, ForeignKey, select, String
from sqlalchemy import orm
from sqlalchemy.orm import selectinload

from models.base_model import Base
from models.exceptions import UserContactNotFound
from loader import session


# TODO мб подумать про repeat кода в create()
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

    last_active: orm.Mapped[int] = orm.mapped_column(
        Integer(),
    )
    registration_time: orm.Mapped[int] = orm.mapped_column(
        Integer(),
    )

    contacts: orm.Mapped[list['UserContact']] = orm.relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    @staticmethod
    async def get_by_telegram_id(telegram_id: int) -> User | None:
        # TODO оптимизация запросов
        return await session.scalar(
            select(User).where(User.telegram_id == telegram_id)
            .outerjoin(UserContact)
            .options(selectinload(User.contacts)),
        )

    @staticmethod
    async def create(telegram_id: int, name: str,
                     telegram_username: str | None = None) -> User:
        user = User(
            telegram_id=telegram_id,
            name=name,
            telegram_username=telegram_username,
            last_active=time.time(),
            registration_time=time.time(),
        )

        session.add(user)
        await session.commit()

        return user


# TODO ограничить число контактов
class UserContact(Base):
    __tablename__ = 'user_contact'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    user_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("user.id"))
    user: orm.Mapped[User] = orm.relationship(back_populates="contacts")

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
    async def get(contact_id: int, **kwargs) -> UserContact:
        query = select(UserContact).where(UserContact.id == contact_id)

        for key, value in kwargs.items():
            query = query.filter(getattr(UserContact, key) == value)

        contact = await session.scalar(query)
        if contact is None:
            raise UserContactNotFound

        return contact

    @staticmethod
    async def delete(contact_id: int) -> None:
        await session.delete(await UserContact.get(contact_id))
        await session.commit()
