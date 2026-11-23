
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import verificar_senha
from app.core.auth import criar_token_acesso
from app.core.models.professor_model import ProfessorModel
from app.core.models.aluno_model import AlunoModel
from app.core.deps import get_usuario_atual


router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login")
async def login(
    dados: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        # Primeiro, verifica se o e-mail pertence a um professor.
        query_professor = select(ProfessorModel).where(
            ProfessorModel.email == dados.username
        )
        resultado_professor = await session.execute(query_professor)
        professor = resultado_professor.scalar_one_or_none()

        if professor:
            usuario = professor
            tipo_usuario = "professor"
        else:
            # Se não for professor, verifica se é aluno.
            query_aluno = select(AlunoModel).where(
                AlunoModel.email == dados.username
            )
            resultado_aluno = await session.execute(query_aluno)
            aluno = resultado_aluno.scalar_one_or_none()

            if aluno:
                usuario = aluno
                tipo_usuario = "aluno"
            else:
                usuario = None
                tipo_usuario = None

        # Valida a existência do usuário e a senha.
        if not usuario or not verificar_senha(dados.password, usuario.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos.",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Cria o token identificando o tipo de usuário.
        token = criar_token_acesso({
            "sub": usuario.email,
            "tipo": tipo_usuario
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "tipo_usuario": tipo_usuario
        }


@router.get("/me")
async def usuario_atual(
    dados: dict = Depends(get_usuario_atual)
):
    usuario = dados["usuario"]

    if dados["tipo"] == "professor":
        identificador = usuario.id_professor
    else:
        identificador = usuario.id_institucional

    return {
        "id": identificador,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo_usuario": dados["tipo"]
    }
