
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import decodificar_token
from app.core.database import get_session
from app.core.models.professor_model import ProfessorModel
from app.core.models.aluno_model import AlunoModel

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

async def get_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_session)
):
    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        dados_token = decodificar_token(token)
        email = dados_token.get("sub")
        tipo_usuario = dados_token.get("tipo")
        if not email or tipo_usuario not in ["aluno", "professor"]:
            raise credenciais_invalidas
    except Exception:
        raise credenciais_invalidas
    async with db as session:
        if tipo_usuario == "professor":
            query = select(ProfessorModel).where(
                ProfessorModel.email == email
            )
        else:
            query = select(AlunoModel).where(
                AlunoModel.email == email
            )
        resultado = await session.execute(query)
        usuario = resultado.scalar_one_or_none()
        if usuario is None:
            raise credenciais_invalidas
        return {
            "usuario": usuario,
            "tipo": tipo_usuario
        }

async def get_professor_atual(
    dados: dict = Depends(get_usuario_atual)
):
    if dados["tipo"] != "professor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido somente para professores."
        )
    return dados["usuario"]

async def get_aluno_atual(
    dados: dict = Depends(get_usuario_atual)
):
    if dados["tipo"] != "aluno":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido somente para alunos."
        )
    return dados["usuario"]

async def get_professor_ou_aluno(
    dados: dict = Depends(get_usuario_atual)
):
    return dados
