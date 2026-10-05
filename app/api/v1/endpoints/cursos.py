from fastapi import APIRouter, Depends, HTTPException, status,Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_session
from app.models.curso_model import CursoModel
from app.schemas.curso import CursoSchema
from sqlalchemy.exc import IntegrityError

router=APIRouter(prefix="/curso")

@router.post(
    "/",
    response_model=CursoSchema,
    status_code=status.HTTP_201_CREATED
)
async def post_curso(
    curso: CursoSchema,
    db: AsyncSession = Depends(get_session)
):
    curso_novo: CursoModel = CursoModel(
        nome=curso.nome,
        hora=curso.hora,
        ementa=curso.ementa
    )

    async with db as session:
        session.add(curso_novo)

        await session.commit()
        await session.refresh(curso_novo)

        return curso_novo
    
@router.get("/", response_model=List[CursoSchema], status_code=status.HTTP_200_OK)
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos = result.scalars().unique().all()
        return cursos

@router.get("/{curso_id}",response_model=CursoSchema)
async def get_curso(curso_id:int,db:AsyncSession=Depends(get_session)):
    async with db as session:
            query=select(CursoModel).filter(CursoModel.id_curso==id_curso)
            result= await session.execute(query)
            curso = result.unique().scalar_one_or_none()

            if curso:
                return curso
            raise HTTPException(
                detail=f"curso com id {curso_id} não encontrado.",
                status_code=status.HTTP_404_NOT_FOUND
            )
@router.put("/{curso_id}", response_model=CursoSchema,status_code=status.HTTP_202_ACCEPTED)
async def put_aluno(curso_id:int,curso:CursoSchema, db:AsyncSession=Depends(get_session)):
    async with db as session:
        query=select(CursoSchema).filter(CursoModel.id_institucional == curso_id)
        result=await session.execute(query)
        curso_up: CursoSchema = result.unique().scalar_one_or_none()
        if curso_up:

            if curso_up.nome:
                curso_up.nome = curso_up.nome
            if curso_up.hora:
                curso_up.hora = curso_up.hora
            if curso_up.ementa:
                 curso_up.ementa = curso_up.ementa
            await session.commit()

            return curso_up

        else:

            raise HTTPException(
                detail=f"curso com id {curso_id} não encontrado.",
                status_code=status.HTTP_404_NOT_FOUND
            )

@router.delete("/{curso_id}", response_model=CursoSchema,status_code=status.HTTP_202_ACCEPTED)
async def delete_aluno(curso_id:int,curso:CursoSchema, db:AsyncSession=Depends(get_session)):
    async with db as session:
        query=select(CursoSchema).filter(CursoModel.id_institucional == curso_id)
        result=await session.execute(query)
        curso_del: CursoSchema = result.unique().scalar_one_or_none()
    if curso_del:
        await session.delete(curso_del)
        await session.commit()
        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
    raise HTTPException(
                    detail=f"curso com id {curso_id} não encontrado.",
                    status_code=status.HTTP_404_NOT_FOUND
                )