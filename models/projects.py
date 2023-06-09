from __future__ import annotations

from sqlalchemy import Boolean, delete, ForeignKey, orm, select, String

from loader import session
from models import InviteToEmployee, User
from models.base_model import Base
from models.exceptions import ProjectNotFound
from models.validators import StringValidator


class Project(Base):
    __tablename__ = 'project'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    name: orm.Mapped[str] = orm.mapped_column(String(30))
    description: orm.Mapped[str] = orm.mapped_column(String(300))
    logo_image_id: orm.Mapped[str] = orm.mapped_column(String(100))

    project_url: orm.Mapped[str] = orm.mapped_column(
        String(200),
        default='',
    )

    show_for_matching: orm.Mapped[bool] = orm.mapped_column(
        Boolean,
        default=False,
    )

    employees: orm.Mapped[list['Employee']] = orm.relationship(
        back_populates='project', cascade='all, delete-orphan',
    )

    users: orm.Mapped[list[User]] = orm.relationship(
        secondary='employee', back_populates='projects',
    )
    candidates: orm.Mapped[list['Candidate']] = orm.relationship(
        back_populates='project', cascade='all, delete-orphan',
    )

    matched_projects: orm.Mapped[list['ProjectMatched']] = orm.relationship(
        back_populates='project'
    )

    invites_to_employee: orm.Mapped[list['InviteToEmployee']] = (
        orm.relationship(
            back_populates='project',
            cascade='all, delete-orphan',
        )
    )

    def check_valid(self):
        max_name_length = self.__table__.c.name.type.length
        StringValidator(max_length=max_name_length).is_valid(
            self.name, 'названия',
        )

        max_desc_length = self.__table__.c.description.type.length
        StringValidator(max_length=max_desc_length).is_valid(
            self.description, 'описания',
        )

        max_logo_length = self.__table__.c.logo_image_id.type.length
        StringValidator(max_length=max_logo_length).is_valid(
            self.logo_image_id, 'изображения',  # TODO тут кринжа
        )

        max_project_url_length = self.__table__.c.project_url.type.length
        StringValidator(
            max_length=max_project_url_length,
            min_length=0,
        ).is_valid(self.project_url)

    async def save(self, commit=True) -> None:
        self.check_valid()

        session.add(self)

        if commit:
            await session.commit()

    async def create_project_with_owner(self, owner: User) -> Project:
        # TODO тут бы конечно транзакцию надо
        await self.save()

        employee = Employee(
            is_owner=True,
            project_id=self.id,
            user_id=owner.id,
        )

        await employee.save()

        return self

    @staticmethod
    def get_join_project_query(project_id):
        return (
            select(Project)
            .join(Employee).where(Employee.project_id == project_id)
            .outerjoin(Candidate, (Candidate.project_id == project_id))
            .options(orm.selectinload(Project.candidates))
            .options(orm.selectinload(Project.employees).selectinload(
                Employee.user))
        )

    # TODO какие-то флаги => мб это переделать надо
    @classmethod
    async def get(cls, project_id: int, do_join=False) -> Project:
        query = select(Project)
        if do_join:
            query = cls.get_join_project_query(project_id)

        project = await session.scalar(
            query.where(Project.id == project_id).limit(1),
        )

        if project is None:
            raise ProjectNotFound

        return project

    @staticmethod
    async def get_projects_by_user(user_id: int) -> list[Project]:
        projects = await session.scalars(
            select(Project)
            .join(Employee)
            .where(Employee.user_id == user_id),
        )

        return projects.all()

    @staticmethod
    async def get_invited_projects(user_id: int) -> list[Project]:
        projects = await session.scalars(
            select(Project)
            .join(InviteToEmployee)
            .where(InviteToEmployee.user_id == user_id),
        )

        return projects.all()

    async def update(self, commit=True, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if commit:
            await session.commit()

    @staticmethod
    async def delete_by_id(project_id: int) -> None:
        await session.execute(
            delete(Project)
            .where(Project.id == project_id),
        )
        await session.commit()


class Employee(Base):
    __tablename__ = 'employee'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    role: orm.Mapped[str] = orm.mapped_column(String(30), default='No_role')
    is_owner: orm.Mapped[bool] = orm.mapped_column(Boolean(), default=False)

    project_id: orm.Mapped[int] = orm.mapped_column(ForeignKey('project.id'))
    project: orm.Mapped[Project] = orm.relationship(
        back_populates='employees',
    )

    user_id: orm.Mapped[int] = orm.mapped_column(ForeignKey('user.id'))
    user: orm.Mapped[User] = orm.relationship(
        back_populates='employees',
    )

    async def save(self, commit=True) -> None:
        session.add(self)

        if commit:
            await session.commit()

    @staticmethod
    async def check_user_is_owner(project_id, user_id) -> bool:
        item: Employee = await session.scalar(
            select(Employee)
            .where(Employee.project_id == project_id)
            .where(Employee.user_id == user_id),
        )

        if not item:
            return False

        return item.is_owner

    @classmethod
    async def get(cls, employee_id: int) -> Employee:
        employee = await session.scalar(
            select(Employee)
            .join(User, (User.id == Employee.user_id))
            .options(orm.selectinload(Employee.user))
            .where(Employee.id == employee_id)
            .limit(1),
        )

        if employee is None:
            raise Exception  # TODO ексепшен сюда

        return employee

    @staticmethod
    async def get_by_project_and_user_id(project_id: int,
                                         user_id: int) -> Employee | None:
        return await session.scalar(
            select(Employee)
            .where(Employee.project_id == project_id)
            .where(Employee.user_id == user_id)
            .limit(1),
        )

    async def update(self, commit=True, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if commit:
            await session.commit()

    @staticmethod
    async def delete_by_id(employee_id: int) -> None:
        await session.execute(
            delete(Employee)
            .where(Employee.id == employee_id),
        )
        await session.commit()

    @staticmethod
    async def delete_by_user_and_project_id(user_id: int,
                                            project_id: int) -> None:
        await session.execute(
            delete(Employee)
            .where(Employee.user_id == user_id)
            .where(Employee.project_id == project_id),
        )
        await session.commit()


class Candidate(Base):
    __tablename__ = 'candidate'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    description: orm.Mapped[str] = orm.mapped_column(String(150))
    role: orm.Mapped[str] = orm.mapped_column(String(30))

    project_id: orm.Mapped[int] = orm.mapped_column(ForeignKey('project.id'))
    project: orm.Mapped[Project] = orm.relationship(
        back_populates='candidates',
    )

    async def save(self, commit=True) -> None:
        session.add(self)

        if commit:
            await session.commit()

    @classmethod
    async def get(cls, candidate_id: int) -> Candidate:
        candidate = await session.scalar(
            select(Candidate)
            .where(Candidate.id == candidate_id)
            .limit(1),
        )

        if candidate is None:
            raise Exception  # TODO ексепшен сюда

        return candidate

    async def update(self, commit=True, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if commit:
            await session.commit()

    @staticmethod
    async def delete_by_id(candidate_id: int) -> None:
        await session.execute(
            delete(Candidate)
            .where(Candidate.id == candidate_id),
        )
        await session.commit()
