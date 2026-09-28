from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.matricula_model import MatriculaModel
from app.schemas.matricula import MatriculaSchema

router = APIRouter(
    prefix="/matriculas"
)

@router.post("/", response_model=MatriculaSchema, status_code=status.HTTP_201_CREATED)
async def create_matricula(
    matricula: MatriculaSchema,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        nova_matricula = MatriculaModel(
            id_institucional=matricula.id_institucional,
            id_curso=matricula.id_curso,
            faltas=matricula.faltas,
            grade_de_horarios=matricula.grade_de_horarios,
            notas=matricula.notas
        )

        session.add(nova_matricula)
        await session.commit()
        await session.refresh(nova_matricula)

        return nova_matricula


@router.get("/{matricula_id}", response_model=MatriculaSchema)
async def get_matricula(
    matricula_id: int,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(MatriculaModel).filter(
            MatriculaModel.id_matricula == matricula_id
        )

        result = await session.execute(query)
        matricula = result.scalar_one_or_none()

        if matricula:
            return matricula

        raise HTTPException(
            detail=f"Matrícula com id {matricula_id} não encontrada.",
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.get("/", response_model=list[MatriculaSchema])
async def get_matriculas(
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(MatriculaModel)

        result = await session.execute(query)
        matriculas = result.scalars().all()

        return matriculas


@router.put("/{matricula_id}", response_model=MatriculaSchema)
async def update_matricula(
    matricula_id: int,
    matricula: MatriculaSchema,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(MatriculaModel).filter(
            MatriculaModel.id_matricula == matricula_id
        )

        result = await session.execute(query)
        matricula_db = result.scalar_one_or_none()

        if not matricula_db:
            raise HTTPException(
                detail=f"Matrícula com id {matricula_id} não encontrada.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        matricula_db.id_institucional = matricula.id_institucional
        matricula_db.id_curso = matricula.id_curso
        matricula_db.faltas = matricula.faltas
        matricula_db.grade_de_horarios = matricula.grade_de_horarios
        matricula_db.notas = matricula.notas

        await session.commit()
        await session.refresh(matricula_db)

        return matricula_db


@router.delete("/{matricula_id}")
async def delete_matricula(
    matricula_id: int,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(MatriculaModel).filter(
            MatriculaModel.id_matricula == matricula_id
        )

        result = await session.execute(query)
        matricula = result.scalar_one_or_none()

        if not matricula:
            raise HTTPException(
                detail=f"Matrícula com id {matricula_id} não encontrada.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        await session.delete(matricula)
        await session.commit()

        return {
            "mensagem": f"Matrícula com id {matricula_id} excluída com sucesso."
        }