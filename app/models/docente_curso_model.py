from sqlalchemy import Column, Integer, ForeignKey
from core.configs import settings

from models.professor_model import ProfessorModel
from models.curso_model import CursoModel


class DocenteModel(settings.DBBaseModel):

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