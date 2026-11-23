import pytest

@pytest.mark.asyncio
async def test_login_professor(client, usuarios_teste):
    resposta = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "professor@teste.com",
            "password": "Professor@123"
        }
    )
    assert resposta.status_code == 200
    assert resposta.json()["tipo_usuario"] == "professor"
    assert "access_token" in resposta.json()

@pytest.mark.asyncio
async def test_login_aluno(client, usuarios_teste):
    resposta = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "aluno@teste.com",
            "password": "Aluno@123"
        }
    )
    assert resposta.status_code == 200
    assert resposta.json()["tipo_usuario"] == "aluno"
    assert "access_token" in resposta.json()

@pytest.mark.asyncio
async def test_login_senha_incorreta(client, usuarios_teste):
    resposta = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "aluno@teste.com",
            "password": "SenhaErrada123"
        }
    )

    assert resposta.status_code == 401

@pytest.mark.asyncio
async def test_login_email_inexistente(client, usuarios_teste):
    resposta = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "inexistente@teste.com",
            "password": "Senha123"
        }
    )
    assert resposta.status_code == 401

@pytest.mark.asyncio
async def test_acesso_me_sem_token(client):
    resposta = await client.get("/api/v1/auth/me")

    assert resposta.status_code == 401


@pytest.mark.asyncio
async def test_me_retorna_dados_do_professor(client, usuarios_teste):
    login = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "professor@teste.com",
            "password": "Professor@123"
        }
    )
    token = login.json()["access_token"]
    resposta = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 200
    assert resposta.json()["tipo_usuario"] == "professor"
    assert resposta.json()["email"] == "professor@teste.com"

@pytest.mark.asyncio
async def test_me_retorna_dados_do_aluno(client, usuarios_teste):
    login = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "aluno@teste.com",
            "password": "Aluno@123"
        }
    )
    token = login.json()["access_token"]
    resposta = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 200
    assert resposta.json()["tipo_usuario"] == "aluno"
    assert resposta.json()["email"] == "aluno@teste.com"
