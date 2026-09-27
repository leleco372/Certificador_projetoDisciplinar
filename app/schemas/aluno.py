from typing import Optional
from pydantic import BaseModel as SCBaseModel, ConfigDict

class AlunoSchema(SCBaseModel):

    id_institucional: Optional[int] = None

    nome: str

    senha: int

    email: int

    model_config = ConfigDict(from_attributes=True)