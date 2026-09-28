from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.professor_model import ProfessorModel
from app.schemas.professor import ProfessorSchema

router = APIRouter(
    prefix="/professores"
)

@router.post("/", response_model=ProfessorSchema, status_code=status.HTTP_201_CREATED)
async def create_professor(
    professor: ProfessorSchema,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        novo_professor = ProfessorModel(
            email=professor.email,
            nome=professor.nome,
            senha=professor.senha
        )

        session.add(novo_professor)
        await session.commit()
        await session.refresh(novo_professor)

        return novo_professor


@router.get("/{professor_id}", response_model=ProfessorSchema)
async def get_professor(
    professor_id: int,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(ProfessorModel).filter(
            ProfessorModel.id_professor == professor_id
        )

        result = await session.execute(query)
        professor = result.scalar_one_or_none()

        if professor:
            return professor

        raise HTTPException(
            detail=f"Professor com id {professor_id} não encontrado.",
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.get("/", response_model=list[ProfessorSchema])
async def get_professores(
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(ProfessorModel)

        result = await session.execute(query)
        professores = result.scalars().all()

        return professores


@router.put("/{professor_id}", response_model=ProfessorSchema)
async def update_professor(
    professor_id: int,
    professor: ProfessorSchema,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(ProfessorModel).filter(
            ProfessorModel.id_professor == professor_id
        )

        result = await session.execute(query)
        professor_db = result.scalar_one_or_none()

        if not professor_db:
            raise HTTPException(
                detail=f"Professor com id {professor_id} não encontrado.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        professor_db.email = professor.email
        professor_db.nome = professor.nome
        professor_db.senha = professor.senha

        await session.commit()
        await session.refresh(professor_db)

        return professor_db


@router.delete("/{professor_id}")
async def delete_professor(
    professor_id: int,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(ProfessorModel).filter(
            ProfessorModel.id_professor == professor_id
        )

        result = await session.execute(query)
        professor = result.scalar_one_or_none()

        if not professor:
            raise HTTPException(
                detail=f"Professor com id {professor_id} não encontrado.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        await session.delete(professor)
        await session.commit()

        return {
            "mensagem": f"Professor com id {professor_id} excluído com sucesso."
        }