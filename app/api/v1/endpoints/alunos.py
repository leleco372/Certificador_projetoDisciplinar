from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.core.models.aluno_model import AlunoModel
from app.schemas.aluno import AlunoSchema, AlunoRespostaSchema
from app.core.database import get_session
from app.core.security import gerar_hash_senha
from app.core.deps import get_professor_atual


router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=AlunoRespostaSchema
)
async def post_usuario(
    aluno: AlunoSchema,
    db: AsyncSession = Depends(get_session),
    professor=Depends(get_professor_atual)
):
    aluno_novo = AlunoModel(
        nome=aluno.nome,
        email=aluno.email,
        senha=gerar_hash_senha(aluno.senha)
    )

    try:
        async with db as session:
            session.add(aluno_novo)
            await session.commit()
            await session.refresh(aluno_novo)
            return aluno_novo

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="email já cadastrado"
        )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[AlunoRespostaSchema]
)
async def get_usuarios(
    db: AsyncSession = Depends(get_session),
    professor=Depends(get_professor_atual)
):
    async with db as session:
        query = select(AlunoModel)
        result = await session.execute(query)
        alunos = result.scalars().all()
        return alunos


@router.get(
    "/{aluno_id}",
    response_model=AlunoRespostaSchema
)
async def get_aluno(
    aluno_id: int,
    db: AsyncSession = Depends(get_session),
    professor=Depends(get_professor_atual)
):
    async with db as session:
        query = select(AlunoModel).filter(
            AlunoModel.id_institucional == aluno_id
        )

        result = await session.execute(query)
        aluno = result.unique().scalar_one_or_none()

        if aluno:
            return aluno

        raise HTTPException(
            detail=f"Aluno com id {aluno_id} não encontrado.",
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.put(
    "/{aluno_id}",
    response_model=AlunoRespostaSchema,
    status_code=status.HTTP_202_ACCEPTED
)
async def put_aluno(
    aluno_id: int,
    aluno: AlunoSchema,
    db: AsyncSession = Depends(get_session),
    professor=Depends(get_professor_atual)
):
    query = select(AlunoModel).where(
        AlunoModel.id_institucional == aluno_id
    )

    result = await db.execute(query)
    aluno_up = result.scalar_one_or_none()

    if aluno_up:
        aluno_up.nome = aluno.nome
        aluno_up.email = aluno.email
        aluno_up.senha = gerar_hash_senha(aluno.senha)

        await db.commit()
        await db.refresh(aluno_up)

        return aluno_up

    raise HTTPException(
        detail=f"Aluno com id {aluno_id} não encontrado.",
        status_code=status.HTTP_404_NOT_FOUND
    )


@router.delete(
    "/{aluno_id}",
    status_code=status.HTTP_200_OK
)
async def delete_aluno(
    aluno_id: int,
    db: AsyncSession = Depends(get_session),
    professor=Depends(get_professor_atual)
):
    async with db as session:
        query = select(AlunoModel).filter(
            AlunoModel.id_institucional == aluno_id
        )

        result = await session.execute(query)
        aluno_del = result.unique().scalar_one_or_none()

        if aluno_del:
            await session.delete(aluno_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(
            detail=f"Aluno com id {aluno_id} não encontrado.",
            status_code=status.HTTP_404_NOT_FOUND
        )
