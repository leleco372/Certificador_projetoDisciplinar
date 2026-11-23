# Certificador_projetoDisciplinar

API RESTful para gerenciamento de eventos e atividades acadêmicas, desenvolvida com Python e FastAPI. O sistema tem como objetivo centralizar e organizar o gerenciamento das informações acadêmicas, substituindo controles manuais por uma solução estruturada e eficiente.

A aplicação possui integração com banco de dados MySQL utilizando SQLAlchemy assíncrono, permitindo realizar operações de cadastro, consulta, atualização e exclusão de dados através dos endpoints da API.

O projeto utiliza Models e Schemas para estruturar os dados, além de chaves primárias, chaves estrangeiras e relacionamentos entre as entidades do sistema.

Também possui autenticação baseada em JWT e controle de acesso para os perfis de Aluno e Professor, garantindo que cada usuário tenha acesso às funcionalidades permitidas.

---

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLAlchemy Async
- MySQL
- Pydantic
- Pydantic Settings
- Uvicorn
- Aiomysql
- PyJWT
- pwdlib
- Pytest
- HTTPX
- aiosqlite
- pytest-asyncio

---

## Funcionalidades

### Gerenciamento acadêmico

- Gerenciamento de alunos.
- Gerenciamento de professores.
- Gerenciamento de cursos.
- Gerenciamento de atividades.
- Gerenciamento de matrículas.
- Operações CRUD.
- Integração com banco de dados MySQL.
- Consultas e manipulação de dados através da API.
- Utilização de chaves primárias e estrangeiras.
- Validação de dados através do Pydantic.
- Tratamento de erros de integridade do banco.
- Utilização de sessões assíncronas.

### Autenticação e controle de acesso

- Autenticação de usuários por e-mail e senha.
- Geração de tokens JWT.
- Identificação dos perfis de Aluno e Professor.
- Validação do token de acesso nas rotas protegidas.
- Controle de acesso baseado no tipo de usuário.
- Diferenciação entre erros de autenticação (401) e autorização (403).
- Restrição de acesso às matrículas de outros alunos.
- Proteção de endpoints contra operações não autorizadas.

---

## Banco de Dados

O projeto utiliza **MySQL** como banco de dados e **SQLAlchemy Async** para realizar a comunicação entre a aplicação e o banco.

A estrutura atual do banco é composta pelas seguintes entidades:

### Aluno

Armazena os dados dos alunos:

- `id_institucional`
- `email`
- `nome`
- `senha`

### Professor

Armazena os dados dos professores:

- `id_professor`
- `email`
- `nome`
- `senha`

### Curso

Armazena as informações dos cursos:

- `id_curso`
- `nome`
- `hora`
- `ementa`

### Atividade

Armazena as atividades relacionadas aos cursos e professores:

- `id_atividade`
- `titulo`
- `data_entrega`
- `descricao`
- `id_curso`
- `id_professor`

As colunas `id_curso` e `id_professor` são utilizadas como chaves estrangeiras.

### Matrícula

Armazena os dados relacionados às matrículas:

- `id_matricula`
- `id_institucional`
- `id_curso`
- `faltas`
- `grade_de_horarios`
- `notas`

O campo `id_curso` possui relacionamento com a tabela de cursos.

---

## Relacionamentos

Os principais relacionamentos definidos no banco envolvem:

- Professor e atividade.
- Curso e atividade.
- Curso e matrícula.

As chaves estrangeiras garantem a integridade dos relacionamentos entre as tabelas.

Exemplos:

```text
atividades.id_professor
        ↓
professores.id_professor
```

```text
atividades.id_curso
        ↓
cursos.id_curso
```

```text
matricula.id_curso
        ↓
cursos.id_curso
```

---

## Integração com o Banco de Dados

A aplicação utiliza o **SQLAlchemy assíncrono** para realizar a comunicação direta com o MySQL.

Através da API é possível executar operações como:

- Inserção de registros.
- Consulta de registros.
- Atualização de registros.
- Exclusão de registros.
- Verificação de registros existentes.
- Validação de chaves estrangeiras.
- Tratamento de erros de integridade.

As sessões de banco de dados são gerenciadas utilizando `AsyncSession`, permitindo que as operações sejam realizadas de forma assíncrona.

---

## Models

Os Models representam as tabelas do banco de dados dentro da aplicação.

Atualmente foram estruturados Models para:

```text
Aluno
Professor
Curso
Atividade
Matrícula
```

Os arquivos dos Models estão organizados em:

```text
app/core/models/
```

Cada Model possui sua respectiva definição de tabela, campos, chaves primárias e, quando necessário, chaves estrangeiras.

---

## Schemas

Os Schemas são utilizados para definir e validar os dados recebidos e enviados pela API.

Foram criados Schemas para as principais entidades do sistema:

```text
Aluno
Professor
Curso
Atividade
Matrícula
```

A aplicação utiliza **Pydantic** para validação e estruturação dos dados.

Também é utilizado:

```python
ConfigDict(from_attributes=True)
```

para permitir a conversão dos objetos do SQLAlchemy em Schemas de resposta.

---

## CRUDs

A API possui estrutura para operações CRUD, permitindo:

```text
CREATE  → Criar registros
READ    → Consultar registros
UPDATE  → Atualizar registros
DELETE  → Excluir registros
```

### Professor

```text
POST   /api/v1/professores/
GET    /api/v1/professores/
GET    /api/v1/professores/{id_professor}
PUT    /api/v1/professores/{id_professor}
DELETE /api/v1/professores/{id_professor}
```

### Matrícula

```text
POST   /api/v1/matriculas/
GET    /api/v1/matriculas/
GET    /api/v1/matriculas/{matricula_id}
PUT    /api/v1/matriculas/{matricula_id}
DELETE /api/v1/matriculas/{matricula_id}
```

### Autenticação

```text
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

O endpoint de login realiza a autenticação do usuário e retorna um token JWT. O endpoint `/auth/me` retorna as informações do usuário autenticado.

Os demais endpoints de gerenciamento acadêmico podem ser consultados na documentação interativa da API.

---

## Autenticação e Controle de Permissões

A aplicação possui autenticação baseada em **JWT (JSON Web Token)**, permitindo identificar os usuários e controlar o acesso aos endpoints protegidos.

O sistema trabalha com dois perfis:

### Professor

O professor possui acesso às funcionalidades administrativas e às operações de gerenciamento previstas para seu perfil.

Entre as operações protegidas estão o gerenciamento de alunos, professores e matrículas.

### Aluno

O aluno possui acesso às funcionalidades permitidas para seu perfil.

No gerenciamento de matrículas, pode consultar seus próprios registros, sem acesso à listagem geral ou às operações administrativas.

### Segurança

A implementação contempla:

- Verificação das credenciais durante o login.
- Geração e validação de tokens JWT.
- Identificação do perfil do usuário autenticado.
- Verificação de permissões antes da execução das operações.
- Retorno HTTP 401 para falhas de autenticação.
- Retorno HTTP 403 para tentativas de acesso não autorizado.

---

## Estrutura do Projeto

```text
Certificador_projetoDisciplinar/
│
├── app/
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── api.py
│   │       └── endpoints/
│   │           ├── alunos.py
│   │           ├── atividades.py
│   │           ├── auth.py
│   │           ├── cursos.py
│   │           ├── matriculas.py
│   │           └── professores.py
│   │
│   ├── core/
│   │   ├── models/
│   │   │   ├── __all_models.py
│   │   │   ├── aluno_model.py
│   │   │   ├── atividade_model.py
│   │   │   ├── curso_model.py
│   │   │   ├── matricula_model.py
│   │   │   └── professor_model.py
│   │   │
│   │   ├── auth.py
│   │   ├── configs.py
│   │   ├── database.py
│   │   ├── deps.py
│   │   └── security.py
│   │
│   ├── schemas/
│   │   ├── aluno.py
│   │   ├── atividade.py
│   │   ├── curso.py
│   │   ├── matricula.py
│   │   └── professor.py
│   │
│   ├── criando_tabelas.py
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_autorizacao.py
│   └── test_funcionalidade.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Configuração do Ambiente

As informações de conexão com o banco de dados e a chave utilizada para autenticação devem ser armazenadas em um arquivo `.env`.

Exemplo:

```env
DB_URL=mysql+aiomysql://usuario:senha@127.0.0.1:3306/sistema_certificacao
JWT_SECRET=sua_chave_secreta
```

O arquivo `.env` não deve ser enviado ao GitHub, pois pode conter informações sensíveis.

A chave JWT deve ser mantida em ambiente privado.

---

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/leleco372/Certificador_projetoDisciplinar.git
```

### 2. Entrar na pasta

```bash
cd Certificador_projetoDisciplinar
```

### 3. Criar o ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Configurar o banco de dados

Crie o banco de dados MySQL e configure as variáveis `DB_URL` e `JWT_SECRET` no arquivo `.env`.

### 7. Executar a aplicação

```bash
python -m uvicorn app.main:app --reload
```

---

## Documentação da API

A aplicação utiliza a documentação automática fornecida pelo FastAPI.

Após iniciar o servidor, a documentação interativa pode ser acessada através do Swagger UI:

```text
http://127.0.0.1:8000/docs
```

O Swagger permite visualizar os endpoints disponíveis e realizar requisições diretamente pelo navegador.

Também é possível acessar a documentação alternativa do FastAPI em:

```text
http://127.0.0.1:8000/redoc
```

---

## Testes Automatizados

O projeto utiliza **Pytest** para executar testes automatizados, verificando o funcionamento da autenticação, das permissões e das operações da API.

Os testes estão organizados na pasta:

```text
tests/
```

### Organização dos testes

| Arquivo | Objetivo |
|---|---|
| `test_auth.py` | Testes de autenticação |
| `test_autorizacao.py` | Testes de autorização e controle de acesso |
| `test_funcionalidade.py` | Testes funcionais das operações de matrícula |
| `conftest.py` | Configuração das fixtures e ambiente de testes |

### Categorias testadas

- Login de Professor e Aluno.
- Login com senha incorreta.
- Login com e-mail inexistente.
- Acesso sem token.
- Retorno dos dados do usuário autenticado.
- Bloqueio de operações não permitidas.
- Acesso permitido para o perfil autorizado.
- Cadastro de matrícula.
- Consulta de matrícula.
- Atualização de matrícula.
- Exclusão de matrícula.
- Consulta de matrícula inexistente.

### Executar os testes

Com as dependências instaladas, execute na raiz do projeto:

```powershell
python -m pytest -v
```

A suíte atual possui **16 testes automatizados**, distribuídos em:

- 7 testes de autenticação.
- 4 testes de autorização.
- 5 testes funcionais.

**Resultado da execução atual: 16 testes aprovados, sem falhas.**

Os testes utilizam SQLite em memória, por meio de `aiosqlite`, para realizar a validação automatizada sem depender do banco de dados MySQL utilizado pela aplicação.

---

## Dependências

As dependências utilizadas pelo projeto estão registradas no arquivo:

```text
requirements.txt
```

Para instalar todas as dependências:

```bash
pip install -r requirements.txt
```

---

## Tratamento de Erros

A aplicação possui tratamento de erros relacionados às operações do banco de dados e às requisições da API.

Entre os casos tratados estão:

- Registros não encontrados.
- E-mails duplicados.
- Chaves estrangeiras inválidas.
- Violações de integridade do banco.
- Falhas de autenticação.
- Tentativas de acesso não autorizado.

O tratamento utiliza exceções do SQLAlchemy, como:

```python
IntegrityError
```

e respostas HTTP através do FastAPI.

---

## Status do Projeto

**Em desenvolvimento.**

O projeto está sendo desenvolvido como parte de um projeto disciplinar.

Até o momento foram implementados:

- Estrutura inicial da aplicação.
- Configuração do FastAPI.
- Configuração do Pydantic Settings.
- Integração com MySQL.
- Configuração do SQLAlchemy assíncrono.
- Configuração do `AsyncSession`.
- Models das entidades.
- Schemas Pydantic.
- Chaves primárias e estrangeiras.
- Relacionamentos entre entidades.
- Criação das tabelas no banco de dados.
- Estrutura dos endpoints.
- Operações CRUD.
- Tratamento de erros de integridade.
- Autenticação com JWT.
- Identificação dos perfis de Aluno e Professor.
- Controle de permissões e proteção de endpoints.
- Restrição de acesso às próprias matrículas para alunos.
- Configuração do Pytest.
- Implementação de 16 testes automatizados.

Novas funcionalidades serão implementadas conforme o desenvolvimento do sistema.

---

## Autores

- **Leandro Ferreira**
- **Maria Julia Vicente**
- **Julio Cesar Bento**
- **Julio Cezar Silvestre**

Projeto desenvolvido para fins acadêmicos.