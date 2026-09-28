from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.docente_curso_model import DocenteCursoModel
from app.schemas.docente_curso import DocenteCursoSchema

router = APIRouter(
    prefix="/docente-curso"
)


@router.post("/", response_model=DocenteCursoSchema, status_code=status.HTTP_201_CREATED)
async def create_docente_curso(
    docente_curso: DocenteCursoSchema,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(DocenteCursoModel).filter(
            DocenteCursoModel.email_professor == docente_curso.email_professor,
            DocenteCursoModel.id_curso == docente_curso.id_curso
        )

        result = await session.execute(query)
        existente = result.scalar_one_or_none()

        if existente:
            raise HTTPException(
                detail="Este professor já está vinculado a este curso.",
                status_code=status.HTTP_409_CONFLICT
            )

        novo_docente_curso = DocenteCursoModel(
            email_professor=docente_curso.email_professor,
            id_curso=docente_curso.id_curso
        )

        session.add(novo_docente_curso)
        await session.commit()
        await session.refresh(novo_docente_curso)

        return novo_docente_curso


@router.get("/{email_professor}/{id_curso}", response_model=DocenteCursoSchema)
async def get_docente_curso(
    email_professor: str,
    id_curso: int,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(DocenteCursoModel).filter(
            DocenteCursoModel.email_professor == email_professor,
            DocenteCursoModel.id_curso == id_curso
        )

        result = await session.execute(query)
        docente_curso = result.scalar_one_or_none()

        if docente_curso:
            return docente_curso

        raise HTTPException(
            detail="Vínculo entre professor e curso não encontrado.",
            status_code=status.HTTP_404_NOT_FOUND
        )


@router.get("/", response_model=list[DocenteCursoSchema])
async def get_docentes_cursos(
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(DocenteCursoModel)

        result = await session.execute(query)
        docentes_cursos = result.scalars().all()

        return docentes_cursos


@router.put("/{email_professor}/{id_curso}", response_model=DocenteCursoSchema)
async def update_docente_curso(
    email_professor: str,
    id_curso: int,
    docente_curso: DocenteCursoSchema,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(DocenteCursoModel).filter(
            DocenteCursoModel.email_professor == email_professor,
            DocenteCursoModel.id_curso == id_curso
        )

        result = await session.execute(query)
        docente_curso_db = result.scalar_one_or_none()

        if not docente_curso_db:
            raise HTTPException(
                detail="Vínculo entre professor e curso não encontrado.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if (
            docente_curso.email_professor != email_professor
            or docente_curso.id_curso != id_curso
        ):
            query = select(DocenteCursoModel).filter(
                DocenteCursoModel.email_professor == docente_curso.email_professor,
                DocenteCursoModel.id_curso == docente_curso.id_curso
            )

            result = await session.execute(query)
            existente = result.scalar_one_or_none()

            if existente:
                raise HTTPException(
                    detail="Este professor já está vinculado a este curso.",
                    status_code=status.HTTP_409_CONFLICT
                )

        docente_curso_db.email_professor = docente_curso.email_professor
        docente_curso_db.id_curso = docente_curso.id_curso

        await session.commit()
        await session.refresh(docente_curso_db)

        return docente_curso_db


@router.delete("/{email_professor}/{id_curso}")
async def delete_docente_curso(
    email_professor: str,
    id_curso: int,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(DocenteCursoModel).filter(
            DocenteCursoModel.email_professor == email_professor,
            DocenteCursoModel.id_curso == id_curso
        )

        result = await session.execute(query)
        docente_curso = result.scalar_one_or_none()

        if not docente_curso:
            raise HTTPException(
                detail="Vínculo entre professor e curso não encontrado.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        await session.delete(docente_curso)
        await session.commit()

        return {
            "mensagem": "Vínculo entre professor e curso excluído com sucesso."
        }