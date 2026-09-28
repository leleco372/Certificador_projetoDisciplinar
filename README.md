# Certificador_projetoDisciplinar

API para gerenciamento de eventos e atividades acadêmicas, desenvolvida com Python e FastAPI. O sistema tem como objetivo centralizar e organizar o gerenciamento das informações acadêmicas, substituindo controles manuais por uma solução estruturada e eficiente.

A aplicação possui integração direta com o banco de dados MySQL utilizando SQLAlchemy assíncrono, permitindo realizar operações de cadastro, consulta, atualização e exclusão de dados através dos endpoints da API.

O projeto utiliza Models e Schemas para estruturar os dados, além de chaves primárias, chaves estrangeiras e relacionamentos entre as entidades do sistema.

---

##  Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLAlchemy Async
- MySQL
- Pydantic
- Pydantic Settings
- Uvicorn
- Aiomysql

---

##  Funcionalidades

- Gerenciamento de alunos
- Gerenciamento de professores
- Gerenciamento de cursos
- Gerenciamento de atividades
- Gerenciamento de matrículas
- Associação entre professores e cursos
- Operações de CRUD
- Integração direta com banco de dados MySQL
- Consultas e manipulação de dados através da API
- Utilização de chaves primárias
- Utilização de chaves estrangeiras
- Relacionamento entre as entidades
- Validação de dados através do Pydantic
- Tratamento de erros de integridade do banco de dados
- Utilização de sessões assíncronas para comunicação com o banco

---

##  Banco de Dados

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

### Docente

A tabela `docente` funciona como uma tabela de associação entre professores e cursos:

- `id_professor`
- `id_curso`

Os dois campos são chaves estrangeiras e também formam uma chave primária composta.

Dessa forma, é possível estabelecer relações entre professores e cursos.

---

##  Relacionamentos

Os principais relacionamentos definidos no banco são:

```text
PROFESSOR
    │
    ├───────────────> ATIVIDADE
    │
    └───────────────> DOCENTE <─────────────── CURSO
                                             │
                                             ├──> ATIVIDADE
                                             │
                                             └──> MATRÍCULA
```

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

```text
docente.id_professor
        ↓
professores.id_professor
```

```text
docente.id_curso
        ↓
cursos.id_curso
```

---

##  Integração com o Banco de Dados

A aplicação utiliza o **SQLAlchemy assíncrono** para realizar a comunicação direta com o MySQL.

Através da API é possível executar operações como:

- Inserção de registros
- Consulta de registros
- Atualização de registros
- Exclusão de registros
- Verificação de registros existentes
- Validação de chaves estrangeiras
- Tratamento de erros de integridade

As sessões de banco de dados são gerenciadas utilizando `AsyncSession`, permitindo que as operações sejam realizadas de forma assíncrona.

---

##  Models

Os Models representam as tabelas do banco de dados dentro da aplicação.

Atualmente foram estruturados Models para:

```text
Aluno
Professor
Curso
Atividade
Matrícula
Docente
```

Cada Model possui sua respectiva definição de tabela, campos, chaves primárias e, quando necessário, chaves estrangeiras.

---

##  Schemas

Os Schemas são utilizados para definir e validar os dados recebidos e enviados pela API.

Foram criados Schemas para as principais entidades do sistema:

```text
Aluno
Professor
Curso
Atividade
Matrícula
Docente
```

A aplicação utiliza **Pydantic** para validação e estruturação dos dados.

Também é utilizado:

```python
ConfigDict(from_attributes=True)
```

para permitir a conversão dos objetos do SQLAlchemy em Schemas de resposta.

---

##  CRUDs

A API possui estrutura para operações CRUD, permitindo:

```text
CREATE  → Criar registros
READ    → Consultar registros
UPDATE  → Atualizar registros
DELETE  → Excluir registros
```

### Professor

```text
POST   /professores/
GET    /professores/
GET    /professores/{id_professor}
PUT    /professores/{id_professor}
DELETE /professores/{id_professor}
```

### Matrícula

```text
POST   /matriculas/
GET    /matriculas/
GET    /matriculas/{id_matricula}
PUT    /matriculas/{id_matricula}
DELETE /matriculas/{id_matricula}
```

### Docente

Como a tabela `docente` utiliza uma chave primária composta por `id_professor` e `id_curso`, suas operações são estruturadas da seguinte forma:

```text
POST   /docentes/
GET    /docentes/
GET    /docentes/{id_professor}/{id_curso}
DELETE /docentes/{id_professor}/{id_curso}
```

A associação de um professor a um curso é realizada através do endpoint de criação de docente.

---

##  Estrutura do Projeto

```text
Certificador_projetoDisciplinar/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── core/
│   │   ├── configs.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── __all_models.py
│   │   ├── aluno_model.py
│   │   ├── professor_model.py
│   │   ├── curso_model.py
│   │   ├── atividade_model.py
│   │   ├── matricula_model.py
│   │   └── docente_curso_model.py
│   │
│   ├── schemas/
│   │   ├── aluno.py
│   │   ├── professor.py
│   │   ├── curso.py
│   │   ├── atividade.py
│   │   ├── matricula.py
│   │   └── docente.py
│   │
│   └── endpoints/
│       ├── api.py
│       ├── alunos.py
│       ├── professores.py
│       ├── cursos.py
│       ├── atividades.py
│       ├── matriculas.py
│       └── docente_curso.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

##  Configuração do Ambiente

As informações de conexão com o banco de dados devem ser armazenadas em um arquivo `.env`.

Exemplo:

```env
DATABASE_URL=mysql+aiomysql://usuario:senha@127.0.0.1:3306/sistema_certificacao
```

O arquivo `.env` não deve ser enviado ao GitHub, pois pode conter informações sensíveis.

Um arquivo `.env.example` pode ser utilizado para demonstrar quais variáveis são necessárias sem expor informações privadas.

---

##  Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone SEU_LINK_DO_REPOSITORIO
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

Crie o banco de dados MySQL e configure a variável `DATABASE_URL` no arquivo `.env`.

Exemplo:

```env
DATABASE_URL=mysql+aiomysql://root:SUA_SENHA@127.0.0.1:3306/sistema_certificacao
```

### 7. Executar a aplicação

```bash
uvicorn app.main:app --reload
```

---

### Documentação da API

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

##  Testes dos Endpoints

Com a aplicação em execução, os endpoints podem ser testados diretamente através do Swagger UI.

Exemplo de criação de professor:

```json
{
    "email": "professor@email.com",
    "nome": "João da Silva",
    "senha": "123456"
}
```

Exemplo de criação de matrícula:

```json
{
    "id_institucional": 2026001,
    "id_curso": 1,
    "faltas": 0,
    "grade_de_horarios": "Segunda e Quarta - 08:00",
    "notas": "8.5"
}
```

Exemplo de associação entre professor e curso:

```json
{
    "id_professor": 1,
    "id_curso": 1
}
```

---

##  Dependências

As dependências utilizadas pelo projeto estão registradas no arquivo:

```text
requirements.txt
```

Para instalar todas as dependências:

```bash
pip install -r requirements.txt
```

---

##  Tratamento de Erros

A aplicação possui tratamento de erros relacionados às operações do banco de dados.

Entre os casos tratados estão:

- Registros não encontrados
- E-mails duplicados
- Chaves estrangeiras inválidas
- Tentativas de criação de relacionamentos duplicados
- Violações de integridade do banco
- Rollback de transações após erros

O tratamento utiliza exceções do SQLAlchemy, como:

```python
IntegrityError
```

e respostas HTTP através do FastAPI.

---

##  Status do Projeto

 **Em desenvolvimento**

O projeto está sendo desenvolvido como parte de um projeto disciplinar.

Até o momento foram implementados:

- Estrutura inicial da aplicação
- Configuração do FastAPI
- Configuração do Pydantic Settings
- Integração com MySQL
- Configuração do SQLAlchemy assíncrono
- Configuração do `AsyncSession`
- Models das entidades
- Schemas Pydantic
- Chaves primárias
- Chaves estrangeiras
- Relacionamentos entre entidades
- Criação das tabelas no banco de dados
- Estrutura dos endpoints
- Operações CRUD
- Tratamento de erros de integridade

Novas funcionalidades serão implementadas conforme o desenvolvimento do sistema.

---

##  Autor

**Leandro Ferreira**

Projeto desenvolvido para fins acadêmicos.