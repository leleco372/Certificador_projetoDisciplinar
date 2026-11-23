import pytest

@pytest.mark.asyncio
async def test_aluno_nao_pode_listar_matriculas(client, usuarios_teste):
    login = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "aluno@teste.com",
            "password": "Aluno@123"
        }
    )
    token = login.json()["access_token"]
    resposta = await client.get(
        "/api/v1/matriculas/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 403

@pytest.mark.asyncio
async def test_professor_pode_listar_matriculas(client, usuarios_teste):
    login = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "professor@teste.com",
            "password": "Professor@123"
        }
    )
    token = login.json()["access_token"]
    resposta = await client.get(
        "/api/v1/matriculas/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 200

@pytest.mark.asyncio
async def test_aluno_pode_visualizar_propria_matricula(client, usuarios_teste):
    login = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "aluno@teste.com",
            "password": "Aluno@123"
        }
    )
    token = login.json()["access_token"]
    resposta = await client.get(
        f"/api/v1/matriculas/{usuarios_teste['matricula_id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 200

@pytest.mark.asyncio
async def test_aluno_nao_pode_excluir_matricula(client, usuarios_teste):
    login = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "aluno@teste.com",
            "password": "Aluno@123"
        }
    )
    token = login.json()["access_token"]
    resposta = await client.delete(
        f"/api/v1/matriculas/{usuarios_teste['matricula_id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 403