from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.atividade_model import AtividadeModel
from app.core.models.matricula_model import MatriculaModel
from app.schemas.atividade import AtividadeCreate, AtividadeUpdate


class AtividadeService:
    @staticmethod
    async def registrar_atividade(
        db: AsyncSession, dados: AtividadeCreate
    ) -> AtividadeModel:
        if getattr(dados, "horas", 1) <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A carga horária da atividade deve ser maior que zero.",
            )

        if hasattr(dados, "matricula_id"):
            matricula = await db.get(MatriculaModel, dados.matricula_id)
            if not matricula:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Matrícula vinculada não encontrada.",
                )

        nova_atividade = AtividadeModel(**dados.model_dump())
        db.add(nova_atividade)
        await db.commit()
        await db.refresh(nova_atividade)
        return nova_atividade

    @staticmethod
    async def atualizar_atividade(
        db: AsyncSession,
        atividade_id: int,
        dados: AtividadeUpdate,
        is_professor_ou_admin: bool,
    ) -> AtividadeModel:
        atividade = await db.get(AtividadeModel, atividade_id)
        if not atividade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Atividade não encontrada.",
            )

        status_atual = getattr(atividade, "status", None)
        if status_atual == "aprovada" and not is_professor_ou_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Atividades já aprovadas não podem ser alteradas pelo aluno.",
            )

        if (
            getattr(dados, "status", None) in {"aprovada", "rejeitada"}
            and not is_professor_ou_admin
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas professores ou administradores podem validar atividades.",
            )

        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(atividade, campo, valor)

        await db.commit()
        await db.refresh(atividade)
        return atividade