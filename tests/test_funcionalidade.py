import pytest

@pytest.mark.asyncio
async def test_professor_cadastra_matricula(client, usuarios_teste):
    login = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "professor@teste.com",
            "password": "Professor@123"
        }
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    novo_aluno = await client.post(
        "/api/v1/alunos/",
        headers=headers,
        json={
            "nome": "Aluno Matrícula Nova",
            "email": "matricula.nova@teste.com",
            "senha": "Aluno@123"
        }
    )
    novo_aluno_id = novo_aluno.json()["id_institucional"]

    resposta = await client.post(
        "/api/v1/matriculas/",
        headers=headers,
        json={
            "id_institucional": novo_aluno_id,
            "id_curso": usuarios_teste["curso_id"],
            "faltas": 0,
            "grade_de_horarios": "Terça-feira",
            "notas": 9
        }
    )
    assert resposta.status_code == 201

@pytest.mark.asyncio
async def test_professor_consulta_matricula(client, usuarios_teste):
    login = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "professor@teste.com",
            "password": "Professor@123"
        }
    )
    token = login.json()["access_token"]
    resposta = await client.get(
        f"/api/v1/matriculas/{usuarios_teste['matricula_id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 200
    assert resposta.json()["id_matricula"] == usuarios_teste["matricula_id"]

@pytest.mark.asyncio
async def test_professor_atualiza_matricula(client, usuarios_teste):
    login = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "professor@teste.com",
            "password": "Professor@123"
        }
    )
    token = login.json()["access_token"]
    resposta = await client.put(
        f"/api/v1/matriculas/{usuarios_teste['matricula_id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "id_institucional": usuarios_teste["aluno_id"],
            "id_curso": usuarios_teste["curso_id"],
            "faltas": 2,
            "grade_de_horarios": "Quarta-feira",
            "notas": 8
        }
    )
    assert resposta.status_code == 200
    assert resposta.json()["faltas"] == 2
    assert resposta.json()["notas"] == 8

@pytest.mark.asyncio
async def test_professor_exclui_matricula(client, usuarios_teste):
    login = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "professor@teste.com",
            "password": "Professor@123"
        }
    )
    token = login.json()["access_token"]
    resposta = await client.delete(
        f"/api/v1/matriculas/{usuarios_teste['matricula_id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 200
    assert "excluída com sucesso" in resposta.json()["mensagem"]

@pytest.mark.asyncio
async def test_consulta_matricula_inexistente(client, usuarios_teste):
    login = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "professor@teste.com",
            "password": "Professor@123"
        }
    )
    token = login.json()["access_token"]
    resposta = await client.get(
        "/api/v1/matriculas/99999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 404
