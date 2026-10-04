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
        String(50),
        nullable=False
    )


    hora = Column(
        String(50),
        nullable=False
    )

    ementa = Column(
        String(255),
        nullable=False
    )