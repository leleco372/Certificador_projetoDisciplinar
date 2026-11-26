from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.aluno_model import AlunoModel
from app.core.models.curso_model import CursoModel
from app.core.models.matricula_model import MatriculaModel
from app.schemas.matricula import MatriculaSchema


class MatriculaService:
    @staticmethod
    async def criar_matricula(
        db: AsyncSession, dados: MatriculaSchema
    ) -> MatriculaModel:
        query_aluno = select(AlunoModel).where(
            AlunoModel.id_institucional == dados.id_institucional
        )
        res_aluno = await db.execute(query_aluno)
        if not res_aluno.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aluno com id {dados.id_institucional} não encontrado.",
            )

        query_curso = select(CursoModel).where(
            CursoModel.id_curso == dados.id_curso
        )
        res_curso = await db.execute(query_curso)
        if not res_curso.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso com id {dados.id_curso} não encontrado.",
            )

        query_dup = select(MatriculaModel).where(
            MatriculaModel.id_institucional == dados.id_institucional,
            MatriculaModel.id_curso == dados.id_curso,
        )
        res_dup = await db.execute(query_dup)
        if res_dup.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aluno já está matriculado neste curso.",
            )

        nova_matricula = MatriculaModel(
            id_institucional=dados.id_institucional,
            id_curso=dados.id_curso,
            faltas=dados.faltas,
            grade_de_horarios=dados.grade_de_horarios,
            notas=str(dados.notas),
        )
        db.add(nova_matricula)
        await db.commit()
        await db.refresh(nova_matricula)
        return nova_matricula