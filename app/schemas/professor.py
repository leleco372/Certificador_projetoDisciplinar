from typing import Optional
from pydantic import BaseModel as SCBaseModel, ConfigDict


class ProfessorSchema(SCBaseModel):
    id_professor: Optional[int] = None
    email: str
    nome: str
    senha: str

    model_config = ConfigDict(from_attributes=True)


class ProfessorRespostaSchema(SCBaseModel):
    id_professor: int
    email: str
    nome: str

    model_config = ConfigDict(from_attributes=True)