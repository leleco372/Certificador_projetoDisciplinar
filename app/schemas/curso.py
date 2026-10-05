from typing import Optional
from pydantic import BaseModel, ConfigDict


class CursoSchema(BaseModel):
    id_curso: Optional[int] = None
    nome: str
    hora: str
    ementa: str

    model_config = ConfigDict(from_attributes=True)