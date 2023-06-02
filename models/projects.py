from models import User
from models.base_model import Base

from sqlalchemy import Boolean, Integer, ForeignKey, orm, select, String
from sqlalchemy_utils import URLType

from loader import session


class Project(Base):
    __tablename__ = 'project'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    name: orm.Mapped[str] = orm.mapped_column(String(30))
    description: orm.Mapped[str] = orm.mapped_column(String(300))
    logo_image_id: orm.Mapped[str] = orm.mapped_column(String(100))

    project_url: orm.Mapped[str] = orm.mapped_column(
        URLType(200),
        nullable=True,
    )

    show_for_matching: orm.Mapped[bool] = orm.mapped_column(
        Boolean,
        default=False,
    )

    users: orm.Mapped[list[User]] = orm.relationship(
        secondary='employee', back_populates='projects',
    )
    candidates: orm.Mapped[list['Candidate']] = orm.relationship(
        back_populates='project', cascade='all, delete-orphan',
    )


class Employee(Base):
    __tablename__ = 'employee'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    role: orm.Mapped[str] = orm.mapped_column(String(30), default='CEO')

    project_id: orm.Mapped[int] = orm.mapped_column(ForeignKey('project.id'))
    user_id: orm.Mapped[int] = orm.mapped_column(ForeignKey('user.id'))


class Candidate(Base):
    __tablename__ = 'candidate'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    description: orm.Mapped[str] = orm.mapped_column(String(150))
    role: orm.Mapped[str] = orm.mapped_column(String(30))

    project_id: orm.Mapped[int] = orm.mapped_column(ForeignKey('project.id'))
    project: orm.Mapped[Project] = orm.relationship(
        back_populates='candidates',
    )
