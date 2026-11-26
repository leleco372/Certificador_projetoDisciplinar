from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_session
from app.core.deps import get_professor_atual, get_usuario_atual
from app.core.models.atividade_model import AtividadeModel
from app.schemas.atividade import AtividadeSchema
from app.services.atividade_service import AtividadeService

router = APIRouter(prefix="/atividades", tags=["Atividades"])


@router.post(
    "/",
    response_model=AtividadeSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_atividade(
    atividade: AtividadeSchema,
    db: AsyncSession = Depends(get_session),
    professor=Depends(get_professor_atual)
):
    async with db as session:
        return await AtividadeService.criar_atividade(session, atividade)


@router.get("/", response_model=List[AtividadeSchema], status_code=status.HTTP_200_OK)
async def get_atividades(
    db: AsyncSession = Depends(get_session),
    usuario=Depends(get_usuario_atual)
):
    async with db as session:
        query = select(AtividadeModel)
        result = await session.execute(query)
        return result.scalars().unique().all()


@router.get("/{atividade_id}", response_model=AtividadeSchema)
async def get_atividade(
    atividade_id: int,
    db: AsyncSession = Depends(get_session),
    usuario=Depends(get_usuario_atual)
):
    async with db as session:
        query = select(AtividadeModel).filter(
            AtividadeModel.id_atividade == atividade_id
        )
        result = await session.execute(query)
        atividade = result.scalar_one_or_none()
        if atividade:
            return atividade
        raise HTTPException(
            detail=f"Atividade com id {atividade_id} não encontrada.",
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.put("/{atividade_id}", response_model=AtividadeSchema)
async def update_atividade(
    atividade_id: int,
    atividade: AtividadeSchema,
    db: AsyncSession = Depends(get_session),
    professor=Depends(get_professor_atual)
):
    async with db as session:
        query = select(AtividadeModel).filter(
            AtividadeModel.id_atividade == atividade_id
        )
        result = await session.execute(query)
        atividade_db = result.scalar_one_or_none()
        if not atividade_db:
            raise HTTPException(
                detail=f"Atividade com id {atividade_id} não encontrada.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        atividade_db.titulo = atividade.titulo
        atividade_db.data_entrega = atividade.data_entrega
        atividade_db.descricao = atividade.descricao
        atividade_db.id_curso = atividade.id_curso
        atividade_db.id_professor = atividade.id_professor
        await session.commit()
        await session.refresh(atividade_db)
        return atividade_db


@router.delete("/{atividade_id}")
async def delete_atividade(
    atividade_id: int,
    db: AsyncSession = Depends(get_session),
    professor=Depends(get_professor_atual)
):
    async with db as session:
        query = select(AtividadeModel).filter(
            AtividadeModel.id_atividade == atividade_id
        )
        result = await session.execute(query)
        atividade = result.scalar_one_or_none()
        if not atividade:
            raise HTTPException(
                detail=f"Atividade com id {atividade_id} não encontrada.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        await session.delete(atividade)
        await session.commit()
        return {
            "mensagem": f"Atividade com id {atividade_id} excluída com sucesso."
        }