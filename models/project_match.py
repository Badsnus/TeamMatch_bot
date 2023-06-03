from sqlalchemy import ForeignKey, orm, select

from loader import session
from models.base_model import Base


class ProjectMatched(Base):
    __tablename__ = 'project_watch'

    project_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey('project.id', ondelete='CASCADE'),
        primary_key=True,
    )
    project: orm.Mapped['Project'] = orm.relationship(
        back_populates='invites_to_employee',
    )

    user_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'),
        primary_key=True,
    )
    user: orm.Mapped['User'] = orm.relationship(
        back_populates='invites_to_employee',
    )

    async def save(self, commit=True) -> None:
        session.add(self)

        if commit:
            await session.commit()
