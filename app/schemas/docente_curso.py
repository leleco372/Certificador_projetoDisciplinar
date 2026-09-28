from pydantic import BaseModel as SCBaseModel, ConfigDict


class DocenteCursoSchema(SCBaseModel):
    id_professor: int
    id_curso: int

    model_config = ConfigDict(from_attributes=True)