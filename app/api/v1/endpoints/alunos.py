from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.aluno_model import AlunoModel
from app.schemas.aluno import AlunoSchema
from app.core.database import get_session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/alunos")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AlunoSchema)
async def post_usuario(aluno: AlunoSchema, db:AsyncSession=Depends(get_session)):
    aluno_novo: AlunoModel = AlunoModel(
        nome=aluno.nome,
        email=aluno.email,
        senha=aluno.senha
    )
    try:
        async with db as session:
            session.add(aluno_novo)
            await session.commit()
            return aluno_novo
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="email já cadastrado")

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[AlunoSchema])
async def get_usuarios(db:AsyncSession=Depends(get_session)):
    async with db as session:
        query=select(AlunoModel)
        result= await session.execute(query)
        alunos: List[AlunoSchema] = result.scalars().all()
        return alunos

@router.get("/{aluno_id}", response_model=AlunoSchema)
async def get_aluno(aluno_id:int, db:AsyncSession=Depends(get_session)):
    async with db as session:
        query=select(AlunoModel).filter(AlunoModel.id_institucional==aluno_id)
        result=await session.execute(query)
        aluno= result.unique().scalar_one_or_none()

        if aluno:
            return aluno
        raise HTTPException(
            detail=f"aluno com id {aluno_id} não encontrado.",
            status_code=status.HTTP_404_NOT_FOUND
        )

@router.put("/{aluno_id}", response_model=AlunoSchema,
            status_code=status.HTTP_202_ACCEPTED)
async def put_aluno(
    aluno_id: int,
    aluno: AlunoSchema,
    db: AsyncSession = Depends(get_session)
):
    query = select(AlunoModel).where(
        AlunoModel.id_institucional == aluno_id
    )

    result = await db.execute(query)
    aluno_up = result.scalar_one_or_none()

    if aluno_up:
        aluno_up.nome = aluno.nome
        aluno_up.email = aluno.email
        aluno_up.senha = aluno.senha

        await db.commit()
        await db.refresh(aluno_up)

        return aluno_up

    else:
        raise HTTPException(
            detail=f"Aluno com id {aluno_id} não encontrado.",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
@router.delete("/{aluno_id}",status_code=status.HTTP_200_OK)
async def delete_aluno(aluno_id:int, db:AsyncSession=Depends(get_session)):
    async with db as session:
            query=select(AlunoModel).filter(AlunoModel.id_institucional == aluno_id)
            result=await session.execute(query)
            aluno_del: AlunoSchema = result.unique().scalar_one_or_none()
            if aluno_del:
                await session.delete(aluno_del)
                await session.commit()
                return Response(
                    status_code=status.HTTP_204_NO_CONTENT
                )