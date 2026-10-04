from sqlalchemy import Column, Integer, String
from app.core.configs import settings


class CursoModel(settings.DBBaseModel):

    __tablename__ = "cursos"

    id_curso = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nome = Column(
        String(50)
    )


    hora = Column(
        String(50)
    )

    ementa = Column(
        String(255)
    )