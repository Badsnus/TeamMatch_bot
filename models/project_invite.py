import asyncio
from typing import Any, Tuple

from sqlalchemy import ForeignKey, orm, select
from sqlalchemy.sql.functions import count

from loader import session
from models.base_model import Base
from utils.send_message_to_user import send_message


class InviteToEmployee(Base):
    __tablename__ = 'invite_to_employee'

    project_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey('project.id'),
        primary_key=True,
    )
    project: orm.Mapped['Project'] = orm.relationship(
        back_populates='invites_to_employee',
    )

    user_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey('user.id'),
        primary_key=True,
    )
    user: orm.Mapped['User'] = orm.relationship(
        back_populates='invites_to_employee',
    )

    async def save(self, commit=True, send_message_to_user=True) -> None:
        session.add(self)

        if commit:
            await session.commit()

        if send_message_to_user:
            asyncio.create_task(
                send_message(
                    message='Ваш пришло новое приглашение в проект',
                    user_id=self.user_id,
                ),
            )

    @staticmethod
    async def get_notice_by_user(user_id: int) -> list['InviteToEmployee']:
        return await session.scalars(
            select(InviteToEmployee).where(InviteToEmployee.user_id == user_id)
        )

    @classmethod
    async def get_notice_count_by_user(cls, user_id: int) -> int:
        return await session.scalar(
            select(count()).where(InviteToEmployee.user_id == user_id)
        )
