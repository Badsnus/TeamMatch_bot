from sqlalchemy import orm, String
from sqlalchemy_utils import URLType

from models.base_model import Base


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
