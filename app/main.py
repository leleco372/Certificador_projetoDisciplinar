from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.api.v1.api import api_router
from app.core.configs import settings
from app.core.database import engine
from app.core.models import __all_models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    yield


tags_metadata = [
    {"name": "Autenticação", "description": "Login via OAuth2/JWT e consulta de perfil autenticado."},
    {"name": "Alunos", "description": "Gerenciamento de alunos cadastrados na instituição."},
    {"name": "Professores", "description": "Gerenciamento de docentes responsáveis pelas disciplinas e atividades."},
    {"name": "Cursos", "description": "Gerenciamento de cursos e cargas horárias."},
    {"name": "Matriculas", "description": "Controle de matrículas, notas e faltas de alunos em cursos."},
    {"name": "Atividades", "description": "Cadastro e acompanhamento de atividades complementares e acadêmicas."},
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "API RESTful para gerenciamento de alunos, professores, cursos, matrículas "
        "e atividades acadêmicas/complementares com autenticação JWT e controle de acesso por perfil."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Violação de integridade: registro duplicado ou referência inválida."},
    )


app.include_router(api_router)