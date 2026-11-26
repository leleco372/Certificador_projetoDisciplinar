from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.aluno_model import AlunoModel
from app.core.models.curso_model import CursoModel
from app.core.models.matricula_model import MatriculaModel
from app.schemas.matricula import MatriculaCreate


class MatriculaService:
    @staticmethod
    async def criar_matricula(
        db: AsyncSession, dados: MatriculaCreate
    ) -> MatriculaModel:
        aluno = await db.get(AlunoModel, dados.aluno_id)
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado.",
            )

        curso = await db.get(CursoModel, dados.curso_id)
        if not curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Curso não encontrado.",
            )

        query = select(MatriculaModel).where(
            MatriculaModel.aluno_id == dados.aluno_id,
            MatriculaModel.curso_id == dados.curso_id,
        )
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aluno já está matriculado neste curso.",
            )

        nova_matricula = MatriculaModel(**dados.model_dump())
        db.add(nova_matricula)
        await db.commit()
        await db.refresh(nova_matricula)
        return nova_matricula

    @staticmethod
    async def deletar_matricula(
        db: AsyncSession,
        matricula_id: int,
        usuario_id: int,
        is_admin: bool,
    ) -> None:
        matricula = await db.get(MatriculaModel, matricula_id)
        if not matricula:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Matrícula não encontrada.",
            )

        if not is_admin and matricula.aluno_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para cancelar matrícula de outro aluno.",
            )

        await db.delete(matricula)
        await db.commit()