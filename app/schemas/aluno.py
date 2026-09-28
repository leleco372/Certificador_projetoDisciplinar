from typing import Optional
from pydantic import BaseModel as SCBaseModel, ConfigDict

class AlunoSchema(SCBaseModel):

    id_institucional: Optional[int] = None

    nome: str

    senha: str
    email: str

    model_config = ConfigDict(from_attributes=True)