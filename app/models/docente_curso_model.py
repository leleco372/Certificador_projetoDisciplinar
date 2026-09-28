from sqlalchemy import Column, Integer, ForeignKey
from app.core.configs import settings

from app.models.professor_model import ProfessorModel
from app.models.curso_model import CursoModel


class DocenteCursoModel(settings.DBBaseModel):

    __tablename__ = "docente"

    id_professor = Column(
        Integer,
        ForeignKey("professores.id_professor"),
        primary_key=True
    )

    id_curso = Column(
        Integer,
        ForeignKey("cursos.id_curso"),
        primary_key=True
    )