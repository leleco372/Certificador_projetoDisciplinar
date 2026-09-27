from sqlalchemy import Column, Integer, String, Date, ForeignKey
from core.configs import settings


class AtividadeModel(settings.DBBaseModel):

    __tablename__ = "atividades"

    id_atividade = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    titulo = Column(
        String(100),
        nullable=False
    )

    data_entrega = Column(Date)

    descricao = Column(String(500))

    id_curso = Column(
        Integer,
        ForeignKey("cursos.id_curso")
    )

    id_professor = Column(
        Integer,
        ForeignKey("professores.id_professor")
    )