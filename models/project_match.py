from __future__ import annotations

from sqlalchemy import ForeignKey, orm, select, and_
from sqlalchemy.orm import selectinload

from loader import session
from models import Candidate, Employee, Project, User
from models.base_model import Base


class ProjectMatched(Base):
    __tablename__ = 'project_watch'

    project_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey('project.id', ondelete='CASCADE'),
        primary_key=True,
    )
    project: orm.Mapped['Project'] = orm.relationship(
        back_populates='matched_projects',
    )

    user_id: orm.Mapped[int] = orm.mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'),
        primary_key=True,
    )

    async def save(self, commit=True) -> None:
        session.add(self)

        if commit:
            await session.commit()

    @staticmethod
    async def get_project_without_match(user_id: int) -> int | None:
        return await session.scalar(
            select(Project)
            .outerjoin(Employee, and_(Employee.project_id == Project.id,
                                      Employee.user_id == user_id))
            .join(ProjectMatched, isouter=True)
            .where(ProjectMatched.project_id.is_(None))
            .where(Employee.id.is_(None))
            .where(Project.show_for_matching == True)
            .order_by(Project.id)
            .limit(1)
            .with_only_columns(Project.id)
        )
