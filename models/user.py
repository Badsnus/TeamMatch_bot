from __future__ import annotations

import time

from sqlalchemy import Integer, select, String
from sqlalchemy import orm

from models.base_model import Base
from loader import session


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

    @staticmethod
    async def get_by_telegram_id(telegram_id) -> User | None:
        return await session.scalar(
            select(User).where(User.telegram_id == telegram_id),
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
