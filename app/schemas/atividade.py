from typing import Optional
from datetime import date

from pydantic import BaseModel as SCBaseModel, ConfigDict


class AtividadeSchema(SCBaseModel):

    id_atividade: Optional[int] = None

    titulo: str

    data_entrega: Optional[date] = None

    descricao: Optional[str] = None

    id_curso: Optional[int] = None

    id_professor: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)