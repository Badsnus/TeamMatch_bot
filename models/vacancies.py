from __future__ import annotations

from sqlalchemy import orm, select, String
from sqlalchemy_utils import URLType

from loader import session
from models.base_model import Base
from models.exceptions import VacancyNotFound


class Vacancy(Base):
    # TODO пока в мвп будут просто линки, потом надо сделать по адекватному с
    # разделением на компании, стек технологий и прочего
    # так же надо будет потом добавить фильтры по юзерам, типа чтобы
    # они не смотрели одну и ту же вакансию кучу раз
    __tablename__ = 'vacancy'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    title: orm.Mapped[str] = orm.mapped_column(String(40))
    description: orm.Mapped[str] = orm.mapped_column(String(400))
    image_id: orm.Mapped[str] = orm.mapped_column(String(100))
    url_for_response: orm.Mapped[str] = orm.mapped_column(URLType())

    @staticmethod
    async def create(user_id: int, name: str, link: str) -> Vacancy:
        vacancy = Vacancy(
            user_id=user_id,
            name=name,
            link=link,
        )

        session.add(vacancy)
        await session.commit()

        return vacancy

    @staticmethod
    async def get(vacancy_id: int) -> Vacancy:
        vacancy = await session.scalar(
            select(Vacancy).where(Vacancy.id == vacancy_id).limit(1),
        )

        if vacancy is None:
            raise VacancyNotFound

        return vacancy

    @staticmethod
    async def get_object_by_filters(*filters) -> list[Vacancy]:
        query = select(Vacancy)

        for f in filters:
            query = query.filter(f)

        vacancy = await session.scalar(query.limit(1))
        if not vacancy:
            raise VacancyNotFound

        return vacancy
