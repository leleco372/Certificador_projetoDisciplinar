import pytest
from datetime import date, timedelta


async def obter_token(client, email: str, senha: str) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": senha},
    )
    if response.status_code != 200:
        response = await client.post(
            "/api/v1/login",
            data={"username": email, "password": senha},
        )
    assert response.status_code == 200, f"Falha no login: {response.text}"
    return response.json()["access_token"]


# TESTES POSITIVOS (CRUD COMPLETO)


@pytest.mark.asyncio
async def test_01_professor_cria_aluno_sucesso(client, usuarios_teste):
    token = await obter_token(client, "professor@teste.com", "Professor@123")
    payload = {
        "nome": "Novo Aluno",
        "email": "novo.aluno@teste.com",
        "senha": "Senha@123"
    }
    response = await client.post(
        "/api/v1/alunos/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "novo.aluno@teste.com"
    assert "senha" not in data


@pytest.mark.asyncio
async def test_02_professor_cria_professor_sucesso(client, usuarios_teste):
    token = await obter_token(client, "professor@teste.com", "Professor@123")
    payload = {
        "nome": "Novo Professor",
        "email": "novo.prof@teste.com",
        "senha": "Senha@123"
    }
    response = await client.post(
        "/api/v1/professores/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "novo.prof@teste.com"
    assert "senha" not in data


@pytest.mark.asyncio
async def test_03_listar_alunos_autenticado(client, usuarios_teste):
    token = await obter_token(client, "professor@teste.com", "Professor@123")
    response = await client.get(
        "/api/v1/alunos/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_04_buscar_aluno_por_id_sucesso(client, usuarios_teste):
    token = await obter_token(client, "professor@teste.com", "Professor@123")
    aluno_id = usuarios_teste["aluno_id"]
    response = await client.get(
        f"/api/v1/alunos/{aluno_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id_institucional"] == aluno_id


@pytest.mark.asyncio
async def test_05_professor_atualiza_dados_aluno_sucesso(client, usuarios_teste):
    token = await obter_token(client, "professor@teste.com", "Professor@123")
    aluno_id = usuarios_teste["aluno_id"]
    payload = {
        "nome": "Aluno Teste Atualizado",
        "email": "aluno@teste.com",
        "senha": "Aluno@123"
    }
    response = await client.put(
        f"/api/v1/alunos/{aluno_id}",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code in (200, 202)
    assert response.json()["nome"] == "Aluno Teste Atualizado"


@pytest.mark.asyncio
async def test_06_professor_cria_atividade_sucesso(client, usuarios_teste):
    token = await obter_token(client, "professor@teste.com", "Professor@123")
    payload = {
        "titulo": "Seminário de FastAPI",
        "data_entrega": str(date.today() + timedelta(days=7)),
        "descricao": "Apresentação prática da API.",
        "id_curso": usuarios_teste["curso_id"],
        "id_professor": usuarios_teste["professor_id"]
    }
    response = await client.post(
        "/api/v1/atividades/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["titulo"] == "Seminário de FastAPI"


@pytest.mark.asyncio
async def test_07_listar_atividades_sucesso(client, usuarios_teste):
    token = await obter_token(client, "aluno@teste.com", "Aluno@123")
    response = await client.get(
        "/api/v1/atividades/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_08_professor_atualiza_atividade_sucesso(client, usuarios_teste):
    token = await obter_token(client, "professor@teste.com", "Professor@123")
    criada = await client.post(
        "/api/v1/atividades/",
        json={
            "titulo": "Atividade Inicial",
            "data_entrega": str(date.today() + timedelta(days=5)),
            "descricao": "Desc inicial",
            "id_curso": usuarios_teste["curso_id"],
            "id_professor": usuarios_teste["professor_id"]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    atividade_id = criada.json()["id_atividade"]

    response = await client.put(
        f"/api/v1/atividades/{atividade_id}",
        json={
            "titulo": "Atividade Revisada",
            "data_entrega": str(date.today() + timedelta(days=10)),
            "descricao": "Desc atualizada",
            "id_curso": usuarios_teste["curso_id"],
            "id_professor": usuarios_teste["professor_id"]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["titulo"] == "Atividade Revisada"


# TESTES NEGATIVOS E REGRAS DE NEGÓCIO


@pytest.mark.asyncio
async def test_09_rn_impedir_email_aluno_duplicado(client, usuarios_teste):
    token = await obter_token(client, "professor@teste.com", "Professor@123")
    payload = {
        "nome": "Aluno Clone",
        "email": "aluno@teste.com",
        "senha": "Senha@123"
    }
    response = await client.post(
        "/api/v1/alunos/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code in (400, 406, 409)


@pytest.mark.asyncio
async def test_10_rn_impedir_email_professor_duplicado(client, usuarios_teste):
    token = await obter_token(client, "professor@teste.com", "Professor@123")
    payload = {
        "nome": "Professor Clone",
        "email": "professor@teste.com",
        "senha": "Senha@123"
    }
    response = await client.post(
        "/api/v1/professores/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code in (400, 406, 409)


@pytest.mark.asyncio
async def test_11_rn_impedir_matricula_duplicada_mesmo_curso(client, usuarios_teste):
    token = await obter_token(client, "professor@teste.com", "Professor@123")
    payload = {
        "id_institucional": usuarios_teste["aluno_id"],
        "id_curso": usuarios_teste["curso_id"],
        "faltas": 0,
        "grade_de_horarios": "Segunda-feira",
        "notas": 9
    }
    response = await client.post(
        "/api/v1/matriculas/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_12_rn_impedir_matricula_curso_inexistente(client, usuarios_teste):
    token = await obter_token(client, "professor@teste.com", "Professor@123")
    payload = {
        "id_institucional": usuarios_teste["aluno_id"],
        "id_curso": 99999,
        "faltas": 0,
        "grade_de_horarios": "Terça-feira",
        "notas": 8
    }
    response = await client.post(
        "/api/v1/matriculas/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_13_rn_aluno_nao_pode_cadastrar_aluno(client, usuarios_teste):
    token = await obter_token(client, "aluno@teste.com", "Aluno@123")
    payload = {
        "nome": "Aluno Intruso",
        "email": "intruso@teste.com",
        "senha": "Senha@123"
    }
    response = await client.post(
        "/api/v1/alunos/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_14_rn_aluno_nao_pode_criar_atividade(client, usuarios_teste):
    token = await obter_token(client, "aluno@teste.com", "Aluno@123")
    payload = {
        "titulo": "Atividade Irregular",
        "data_entrega": str(date.today() + timedelta(days=5)),
        "descricao": "Aluno tentando criar atividade.",
        "id_curso": usuarios_teste["curso_id"],
        "id_professor": usuarios_teste["professor_id"]
    }
    response = await client.post(
        "/api/v1/atividades/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_15_buscar_aluno_inexistente_retorna_404(client, usuarios_teste):
    token = await obter_token(client, "professor@teste.com", "Professor@123")
    response = await client.get(
        "/api/v1/alunos/99999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_16_buscar_atividade_inexistente_retorna_404(client, usuarios_teste):
    token = await obter_token(client, "professor@teste.com", "Professor@123")
    response = await client.get(
        "/api/v1/atividades/99999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_17_acesso_sem_token_retorna_401(client):
    response = await client.get("/api/v1/alunos/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_18_login_senha_incorreta_retorna_erro(client, usuarios_teste):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "aluno@teste.com", "password": "SenhaErrada@999"},
    )
    if response.status_code == 404:
        response = await client.post(
            "/api/v1/login",
            data={"username": "aluno@teste.com", "password": "SenhaErrada@999"},
        )
    assert response.status_code in (400, 401)