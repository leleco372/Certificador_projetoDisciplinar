
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_session
from app.core.deps import get_professor_atual
from app.core.models.curso_model import CursoModel
from app.core.models.professor_model import ProfessorModel
from app.schemas.curso import CursoSchema


router = APIRouter(prefix="/curso", tags=["Cursos"])


@router.post(
    "/",
    response_model=CursoSchema,
    status_code=status.HTTP_201_CREATED
)
async def post_curso(
    curso: CursoSchema,
    db: AsyncSession = Depends(get_session),
    professor_atual: ProfessorModel = Depends(get_professor_atual)
):
    async with db as session:
        curso_novo = CursoModel(
            nome=curso.nome,
            hora=curso.hora,
            ementa=curso.ementa
        )

        session.add(curso_novo)
        await session.commit()
        await session.refresh(curso_novo)

        return curso_novo


@router.get(
    "/",
    response_model=List[CursoSchema],
    status_code=status.HTTP_200_OK
)
async def get_cursos(
    db: AsyncSession = Depends(get_session),
    professor_atual: ProfessorModel = Depends(get_professor_atual)
):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos = result.scalars().unique().all()

        return cursos


@router.get("/{curso_id}", response_model=CursoSchema)
async def get_curso(
    curso_id: int,
    db: AsyncSession = Depends(get_session),
    professor_atual: ProfessorModel = Depends(get_professor_atual)
):
    async with db as session:
        query = select(CursoModel).filter(
            CursoModel.id_curso == curso_id
        )

        result = await session.execute(query)
        curso = result.scalar_one_or_none()

        if curso:
            return curso

        raise HTTPException(
            detail=f"Curso com id {curso_id} não encontrado.",
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.put(
    "/{curso_id}",
    response_model=CursoSchema,
    status_code=status.HTTP_202_ACCEPTED
)
async def put_curso(
    curso_id: int,
    curso: CursoSchema,
    db: AsyncSession = Depends(get_session),
    professor_atual: ProfessorModel = Depends(get_professor_atual)
):
    async with db as session:
        query = select(CursoModel).filter(
            CursoModel.id_curso == curso_id
        )

        result = await session.execute(query)
        curso_up = result.scalar_one_or_none()

        if not curso_up:
            raise HTTPException(
                detail=f"Curso com id {curso_id} não encontrado.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        curso_up.nome = curso.nome
        curso_up.hora = curso.hora
        curso_up.ementa = curso.ementa

        await session.commit()
        await session.refresh(curso_up)

        return curso_up


@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(
    curso_id: int,
    db: AsyncSession = Depends(get_session),
    professor_atual: ProfessorModel = Depends(get_professor_atual)
):
    async with db as session:
        query = select(CursoModel).filter(
            CursoModel.id_curso == curso_id
        )

        result = await session.execute(query)
        curso_del = result.scalar_one_or_none()

        if not curso_del:
            raise HTTPException(
                detail=f"Curso com id {curso_id} não encontrado.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        await session.delete(curso_del)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
