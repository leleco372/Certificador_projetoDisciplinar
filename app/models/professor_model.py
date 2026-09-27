from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings

class ProfessorModel(settings.DBBaseModel):
    __tablename__ = "professores"
    id_professor = Column(Integer, primary_key=True,autoincrement=True)
    email = Column(String(255),unique=True,nullable=False)
    nome = Column(String(150),nullable=False)
    senha = Column(String(255),nullable=False)