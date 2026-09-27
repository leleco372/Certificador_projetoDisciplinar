from sqlalchemy import Column, Integer, String
from core.configs import settings


class CursoModel(settings.DBBaseModel):

    __tablename__ = "cursos"

    id_curso = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    hora = Column(
        String(50)
    )

    ementa = Column(
        String(255)
    )