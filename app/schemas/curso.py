from typing import Optional
from pydantic import BaseModel as SCBaseModel, ConfigDict


class CursoSchema(SCBaseModel):
    id_curso: Optional[int] = None
    hora: str
    ementa: str

    model_config = ConfigDict(from_attributes=True)