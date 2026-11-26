from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.atividade_model import AtividadeModel
from app.core.models.curso_model import CursoModel
from app.schemas.atividade import AtividadeSchema


class AtividadeService:
    @staticmethod
    async def criar_atividade(
        db: AsyncSession, dados: AtividadeSchema
    ) -> AtividadeModel:
        if dados.id_curso is not None:
            query_curso = select(CursoModel).where(
                CursoModel.id_curso == dados.id_curso
            )
            res_curso = await db.execute(query_curso)
            if not res_curso.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Curso com id {dados.id_curso} não encontrado.",
                )

        nova_atividade = AtividadeModel(
            titulo=dados.titulo,
            data_entrega=dados.data_entrega,
            descricao=dados.descricao,
            id_curso=dados.id_curso,
            id_professor=dados.id_professor,
        )
        db.add(nova_atividade)
        await db.commit()
        await db.refresh(nova_atividade)
        return nova_atividade