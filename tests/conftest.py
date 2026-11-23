
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.core.configs import settings
from app.core.database import get_session
from app.core.security import gerar_hash_senha
from app.core.models import __all_models
from app.core.models.aluno_model import AlunoModel
from app.core.models.professor_model import ProfessorModel
from app.core.models.curso_model import CursoModel
from app.core.models.matricula_model import MatriculaModel

@pytest_asyncio.fixture
async def test_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    async with engine.begin() as connection:
        await connection.run_sync(
            settings.DBBaseModel.metadata.create_all
        )
    yield engine
    async with engine.begin() as connection:
        await connection.run_sync(
            settings.DBBaseModel.metadata.drop_all
        )
    await engine.dispose()

@pytest_asyncio.fixture
async def client(test_engine):
    TestSession = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False
    )
    async def override_get_session():
        async with TestSession() as session:
            yield session
    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def usuarios_teste(test_engine):
    TestSession = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False
    )
    async with TestSession() as session:
        professor = ProfessorModel(
            nome="Professor Teste",
            email="professor@teste.com",
            senha=gerar_hash_senha("Professor@123")
        )
        aluno = AlunoModel(
            nome="Aluno Teste",
            email="aluno@teste.com",
            senha=gerar_hash_senha("Aluno@123")
        )
        curso = CursoModel(
            nome="Curso de Teste",
            hora="40 horas",
            ementa="Curso utilizado nos testes automatizados."
        )
        session.add_all([professor, aluno, curso])
        await session.flush()
        matricula = MatriculaModel(
            id_institucional=aluno.id_institucional,
            id_curso=curso.id_curso,
            faltas=0,
            grade_de_horarios="Segunda-feira",
            notas=10
        )
        session.add(matricula)
        await session.commit()
        return {
            "professor_id": professor.id_professor,
            "aluno_id": aluno.id_institucional,
            "curso_id": curso.id_curso,
            "matricula_id": matricula.id_matricula
        }
