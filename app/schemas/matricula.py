from typing import Optional
from pydantic import BaseModel as SCBaseModel, ConfigDict


class MatriculaSchema(SCBaseModel):
    id_matricula: Optional[int] = None
    id_institucional: int
    id_curso: int
    faltas: int
    grade_de_horarios: str
    notas: int

    model_config = ConfigDict(from_attributes=True)