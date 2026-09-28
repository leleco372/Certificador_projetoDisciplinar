from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.configs import settings


class MatriculaModel(settings.DBBaseModel):
    __tablename__ = "matricula"

    id_matricula = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_institucional = Column(
        Integer,
        nullable=False
    )

    id_curso = Column(
        Integer,
        ForeignKey("cursos.id_curso"),
        nullable=False
    )

    faltas = Column(
        Integer,
        nullable=False
    )

    grade_de_horarios = Column(
        String(100),
        nullable=False
    )

    notas = Column(
        String(100),
        nullable=False
    )
