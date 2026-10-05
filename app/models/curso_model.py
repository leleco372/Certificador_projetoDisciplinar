
from sqlalchemy import Column, Integer, String
from app.core.configs import settings


class CursoModel(settings.DBBaseModel):
    __tablename__ = "cursos"

    id_curso = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    nome = Column(String, nullable=False)
    hora = Column(String, nullable=False)
    ementa = Column(String, nullable=False)