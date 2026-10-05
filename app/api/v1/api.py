from fastapi import APIRouter

from app.api.v1.endpoints import alunos
from app.api.v1.endpoints import professores
from app.api.v1.endpoints import cursos
from app.api.v1.endpoints.atividadades import router as atividades_router
from app.api.v1.endpoints import matriculas

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(alunos.router)
api_router.include_router(professores.router)
api_router.include_router(cursos.router)
api_router.include_router(atividades_router)
api_router.include_router(matriculas.router)