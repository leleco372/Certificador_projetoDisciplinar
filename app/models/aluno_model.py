from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings
from models.matricula_model import MatriculaModel

class AlunoModel(settings.DBBaseModel):
    __tablename__ = "aluno"
    id_institucional=Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255),unique=True,nullable=False)
    nome = Column(String(150))
    senha = Column(String(255))
    