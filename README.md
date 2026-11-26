# Certificador_projetoDisciplinar

API RESTful para gerenciamento de eventos e atividades acadêmicas, desenvolvida com Python e FastAPI. O sistema tem como objetivo centralizar e organizar o gerenciamento das informações acadêmicas, substituindo controles manuais por uma solução estruturada e eficiente.

A aplicação possui integração com banco de dados relacional (MySQL, PostgreSQL ou SQLite) utilizando SQLAlchemy assíncrono, permitindo realizar operações de cadastro, consulta, atualização e exclusão de dados através dos endpoints da API.

O projeto utiliza Models, Schemas e uma camada dedicada de Services para estruturar os dados e isolar as regras de negócio, além de chaves primárias, chaves estrangeiras e relacionamentos entre as entidades do sistema.

Também possui autenticação baseada em JWT e controle de acesso para os perfis de Aluno e Professor, garantindo que cada usuário tenha acesso às funcionalidades permitidas.

---

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLAlchemy Async
- MySQL / PostgreSQL / SQLite
- Pydantic
- Pydantic Settings
- Uvicorn
- Aiomysql / Asyncpg / Aiosqlite
- PyJWT
- pwdlib
- Pytest
- HTTPX
- pytest-asyncio

---

## Funcionalidades

### Gerenciamento acadêmico

- Gerenciamento de alunos.
- Gerenciamento de professores.
- Gerenciamento de cursos.
- Gerenciamento de atividades.
- Gerenciamento de matrículas.
- Operações CRUD completas.
- Camada de serviços (`services`) para validação de regras de negócio.
- Integração com banco de dados via SQLAlchemy assíncrono.
- Consultas e manipulação de dados através da API.
- Utilização de chaves primárias e estrangeiras.
- Validação de dados através do Pydantic.
- Tratamento global padronizado de erros de integridade do banco.
- Criação automática de tabelas no ciclo de inicialização (`lifespan`).

### Autenticação e controle de acesso

- Autenticação de usuários por e-mail e senha.
- Geração de tokens JWT.
- Identificação dos perfis de Aluno e Professor.
- Validação do token de acesso nas rotas protegidas.
- Controle de acesso baseado no tipo de usuário.
- Diferenciação entre erros de autenticação (401) e autorização (403).
- Restrição de acesso às matrículas de outros alunos.
- Proteção de endpoints administrativos e de cadastro contra operações não autorizadas.

---

## Regras de Negócio

As regras de negócio previstas no escopo do sistema são aplicadas nas camadas de acesso (`deps`) e serviços (`app/services/`):

- **RN01:** Não é permitido cadastrar alunos com e-mail já existente no sistema (`400`/`406`).
- **RN02:** Não é permitido cadastrar professores com e-mail já existente no sistema (`400`).
- **RN03:** Apenas usuários autenticados com perfil de Professor podem cadastrar, atualizar ou excluir alunos, professores e matrículas (`401`/`403`).
- **RN04:** Um aluno não pode ser matriculado mais de uma vez no mesmo curso (`400`).
- **RN05:** Não é permitido realizar matrícula vinculada a aluno ou curso inexistente (`404`).
- **RN06:** Alunos autenticados podem visualizar apenas a própria matrícula, sendo bloqueado o acesso à listagem geral ou a matrículas de terceiros (`403`).
- **RN07:** Apenas professores podem criar, atualizar ou excluir atividades acadêmicas/complementares (`403`).
- **RN08:** Não é permitido vincular uma atividade a um curso inexistente (`404`).
- **RN09:** Senhas de alunos e professores são armazenadas exclusivamente em formato hash e nunca são retornadas nos schemas de resposta.
- **RN10:** Violações de integridade referencial ou unicidade no banco são interceptadas globalmente e padronizadas como erro `400 Bad Request`.

---

## Banco de Dados

O projeto utiliza **SQLAlchemy Async** para realizar a comunicação entre a aplicação e o banco de dados relacional, suportando **MySQL** (`aiomysql`), **PostgreSQL** (`asyncpg`) em produção e **SQLite** (`aiosqlite`) para desenvolvimento local e testes.

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

A aplicação utiliza o **SQLAlchemy assíncrono** para realizar a comunicação direta com o banco de dados configurado em `DB_URL`.

Através da API é possível executar operações como:

- Inserção de registros.
- Consulta de registros.
- Atualização de registros.
- Exclusão de registros.
- Verificação de registros existentes.
- Validação de chaves estrangeiras.
- Tratamento global de erros de integridade.

As sessões de banco de dados são gerenciadas utilizando `AsyncSession`, permitindo que as operações sejam realizadas de forma assíncrona. Na inicialização da aplicação (`lifespan`), as tabelas são criadas automaticamente caso ainda não existam no banco.

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

### Aluno

```text
POST   /api/v1/alunos/
GET    /api/v1/alunos/
GET    /api/v1/alunos/{aluno_id}
PUT    /api/v1/alunos/{aluno_id}
DELETE /api/v1/alunos/{aluno_id}
```

### Professor

```text
POST   /api/v1/professores/
GET    /api/v1/professores/
GET    /api/v1/professores/{id_professor}
PUT    /api/v1/professores/{id_professor}
DELETE /api/v1/professores/{id_professor}
```

### Curso

```text
POST   /api/v1/cursos/
GET    /api/v1/cursos/
GET    /api/v1/cursos/{curso_id}
PUT    /api/v1/cursos/{curso_id}
DELETE /api/v1/cursos/{curso_id}
```

### Atividade

```text
POST   /api/v1/atividades/
GET    /api/v1/atividades/
GET    /api/v1/atividades/{atividade_id}
PUT    /api/v1/atividades/{atividade_id}
DELETE /api/v1/atividades/{atividade_id}
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

---

## Autenticação e Controle de Permissões

A aplicação possui autenticação baseada em **JWT (JSON Web Token)**, permitindo identificar os usuários e controlar o acesso aos endpoints protegidos.

O sistema trabalha com dois perfis:

### Professor

O professor possui acesso às funcionalidades administrativas e às operações de gerenciamento previstas para seu perfil.

Entre as operações protegidas estão o gerenciamento de alunos, professores, cursos, atividades e matrículas.

### Aluno

O aluno possui acesso às funcionalidades permitidas para seu perfil.

No gerenciamento de matrículas, pode consultar seus próprios registros, sem acesso à listagem geral ou às operações administrativas. Pode também consultar as atividades disponíveis.

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
│   ├── services/
│   │   ├── atividade_service.py
│   │   └── matricula_service.py
│   │
│   ├── criando_tabelas.py
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_autorizacao.py
│   ├── test_funcionalidade.py
│   └── test_regras_negocio_crud.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── Procfile
├── README.md
└── requirements.txt
```

---

## Configuração do Ambiente

As informações de conexão com o banco de dados e a chave utilizada para autenticação devem ser armazenadas em um arquivo `.env`, baseado no modelo `.env.example`.

Exemplo:

```env
PROJECT_NAME="Certificador de Atividades Complementares"
API_V1_STR="/api/v1"
DB_URL="sqlite+aiosqlite:///./certificador.db"
JWT_SECRET="sua_chave_secreta"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

O arquivo `.env` está listado no `.gitignore` e não é enviado ao GitHub, evitando exposição de credenciais.

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

### 6. Configurar o ambiente

Copie o arquivo `.env.example` para `.env` e configure as variáveis `DB_URL` e `JWT_SECRET`.

### 7. Executar a aplicação

```bash
python -m uvicorn app.main:app --reload
```

---

## Deploy e Persistência

A aplicação está preparada para publicação em serviços em nuvem (como Render, Railway ou ambientes baseados em contêineres Docker):

- **`Dockerfile` e `.dockerignore`:** Empacotam a aplicação em imagem Python 3.12 slim executando o servidor Uvicorn na porta definida pela variável `PORT`.
- **`Procfile`:** Define o comando de inicialização web (`web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}`).
- **Persistência em Produção:** O módulo `app/core/database.py` converte automaticamente URLs `postgres://` ou `postgresql://` para o driver assíncrono `postgresql+asyncpg://`, enquanto o evento `lifespan` em `app/main.py` garante a criação automática das tabelas no banco de dados configurado.

---

## Documentação da API

A aplicação utiliza a documentação automática fornecida pelo FastAPI, enriquecida com metadados de tags, descrição e esquemas de autenticação JWT.

Após iniciar o servidor, a documentação interativa pode ser acessada através do Swagger UI:

```text
http://127.0.0.1:8000/docs
```

O Swagger permite visualizar os endpoints disponíveis, schemas de entrada/saída e realizar requisições autenticadas diretamente pelo navegador.

Também é possível acessar a documentação alternativa do FastAPI em:

```text
http://127.0.0.1:8000/redoc
```

---

## Testes Automatizados

O projeto utiliza **Pytest** para executar testes automatizados, verificando o funcionamento da autenticação, das permissões, das operações CRUD e das regras de negócio da API.

Os testes estão organizados na pasta:

```text
tests/
```

### Organização dos testes

| Arquivo | Objetivo |
|---|---|
| `test_auth.py` | Testes de autenticação e token JWT |
| `test_autorizacao.py` | Testes de autorização e controle de acesso por perfil |
| `test_funcionalidade.py` | Testes funcionais das operações de matrícula |
| `test_regras_negocio_crud.py` | Testes positivos e negativos de CRUD, regras de negócio e status codes |
| `conftest.py` | Configuração das fixtures e ambiente de testes isolado |

### Categorias testadas

- Login de Professor e Aluno.
- Login com senha incorreta e e-mail inexistente.
- Acesso sem token (`401`) e acesso sem permissão (`403`).
- Retorno dos dados do usuário autenticado (`/auth/me`).
- Cadastro, consulta, listagem e atualização de alunos, professores, matrículas e atividades.
- Bloqueio de e-mail duplicado para alunos e professores.
- Bloqueio de matrícula duplicada no mesmo curso e matrícula em curso inexistente.
- Consulta de registros inexistentes retornando `404`.

### Executar os testes

Com as dependências instaladas, execute na raiz do projeto:

```powershell
python -m pytest -v
```

A suíte atual possui **34 testes automatizados**, distribuídos em:

- 7 testes de autenticação (`test_auth.py`).
- 4 testes de autorização (`test_autorizacao.py`).
- 5 testes funcionais (`test_funcionalidade.py`).
- 18 testes de CRUD, cenários negativos e regras de negócio (`test_regras_negocio_crud.py`).

**Resultado da execução atual: 34 testes aprovados, sem falhas.**

Os testes utilizam SQLite em memória, por meio de `aiosqlite`, para realizar a validação automatizada de forma isolada sem depender de banco de dados externo.

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

A aplicação possui tratamento padronizado de erros relacionados às operações do banco de dados, regras de negócio e requisições da API.

Entre os casos tratados estão:

- Registros não encontrados (`404 Not Found`).
- E-mails duplicados, matrículas duplicadas e violações de integridade referencial (`400 Bad Request` / `406 Not Acceptable`).
- Falhas de autenticação (`401 Unauthorized`).
- Tentativas de acesso ou operação não autorizada por perfil (`403 Forbidden`).
- Erros de validação de payload (`422 Unprocessable Entity`).

Além das validações explícitas nos endpoints e na camada `services`, a aplicação registra um *exception handler* global para `IntegrityError` do SQLAlchemy em `app/main.py`, garantindo respostas JSON consistentes.

---

## Status do Projeto

**Consolidado para entrega.**

O projeto foi desenvolvido como parte de um projeto disciplinar e contempla:

- Estrutura modularizada (`api`, `core`, `models`, `schemas`, `services`).
- Configuração do FastAPI com documentação Swagger/OpenAPI atualizada.
- Configuração de variáveis de ambiente via Pydantic Settings (`.env.example`).
- Integração assíncrona com banco de dados relacional via SQLAlchemy (`AsyncSession`).
- Models, Schemas Pydantic, chaves primárias, chaves estrangeiras e relacionamentos.
- Operações CRUD completas e validação de regras de negócio.
- Tratamento global padronizado de erros de integridade e status codes HTTP.
- Autenticação com JWT e controle de permissões para os perfis de Aluno e Professor.
- Configuração do Pytest com 34 testes automatizados aprovados.
- Arquivos de configuração preparados para deploy (`Dockerfile`, `Procfile` e `.dockerignore`).

---

## Autores

- **Leandro Ferreira**
- **Maria Julia Vicente**
- **Julio Cesar Bento**
- **Julio Cezar Silvestre**

Projeto desenvolvido para fins acadêmicos.