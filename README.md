# 🏠 TemVagaAi - Backend API

> API REST completa para gerenciamento de anúncios de vagas estudantis com **Clean Architecture**, autenticação JWT, upload de imagens e sistema de comentários.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Clean_Architecture-blue)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
[![SOLID](https://img.shields.io/badge/Principles-SOLID-green)](https://en.wikipedia.org/wiki/SOLID)

## ✨ Características Principais

- 🏛️ **Clean Architecture** - Código organizado em 4 camadas bem definidas
- 🎯 **SOLID Principles** - Código limpo, manutenível e escalável
- 🔐 **Autenticação JWT** - Segurança com bcrypt e tokens JWT
- 📝 **Sistema de Rascunhos** - Salve anúncios incompletos como draft
- ⏰ **Republicação Inteligente** - Timestamps atualizados ao republicar
- 🖼️ **Upload de Imagens** - Até 15 imagens por anúncio (5MB cada)
- 💬 **Sistema de Comentários** - Avaliações e feedback dos usuários
- ⭐ **Favoritos** - Sistema de anúncios favoritos sincronizado
- 📊 **Documentação Automática** - Swagger UI e ReDoc integrados
- ✅ **Validação Condicional** - Campos obrigatórios apenas para anúncios publicados

---

## 📋 Requisitos

- Python 3.13 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd Backend-FastAPI
```

### 2. Crie um ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure:

```env
DATABASE_URL=sqlite:///./temvagaai.db
SECRET_KEY=sua-chave-secreta-aqui-mude-em-producao
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

**⚠️ IMPORTANTE:** Gere uma chave secreta segura para produção:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Inicialize o banco de dados

```bash
python init_db.py
```

Este comando irá:
- Criar as tabelas no banco de dados
- Inserir categorias padrão (Apartamento, Casa, Kitnet, Quarto, Residencial)
- Criar um usuário de teste (email: `teste@temvagaai.com`, senha: `senha123`)
- Criar alguns anúncios de exemplo

## ▶️ Executando a aplicação

### Modo rápido (recomendado)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Modo manual

**Desenvolvimento (com auto-reload):**
```bash
uvicorn app.main:app --reload
```

**Produção:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI (interativa):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## 🔐 Autenticação

A API utiliza JWT (JSON Web Token) para autenticação. Para acessar rotas protegidas:

### 1. Registrar um usuário

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "senha123",
    "name": "Seu Nome"
  }'
```

### 2. Fazer login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@example.com&password=senha123"
```

### 3. Usar o token nas requisições

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 📡 Endpoints principais

### Autenticação
- `POST /api/auth/register` - Registrar novo usuário
- `POST /api/auth/login` - Login (OAuth2 form-data)
- `GET /api/auth/me` - Informações do usuário autenticado

### Usuários
- `GET /api/users/me` - Perfil do usuário autenticado 🔒
- `PUT /api/users/me` - Atualizar perfil 🔒
- `DELETE /api/users/me` - Deletar conta 🔒
- `GET /api/users/{user_id}` - Informações públicas de um usuário

### Categorias
- `GET /api/categories` - Listar categorias
- `GET /api/categories/{id}` - Detalhes da categoria
- `POST /api/categories` - Criar categoria 🔒
- `PUT /api/categories/{id}` - Atualizar categoria 🔒
- `DELETE /api/categories/{id}` - Deletar categoria 🔒

### Anúncios
- `GET /api/ads` - Listar anúncios (com filtros: category_id, location, skip, limit)
- `GET /api/ads/me` - Meus anúncios 🔒
- `GET /api/ads/{id}` - Detalhes do anúncio com informações do dono
- `POST /api/ads` - Criar anúncio 🔒
- `PUT /api/ads/{id}` - Atualizar anúncio 🔒
- `DELETE /api/ads/{id}` - Deletar anúncio 🔒

**Status dos anúncios:**
- `draft` - Rascunho (não publicado) - Campos seller/location opcionais
- `published` - Publicado e disponível - Todos os campos obrigatórios
- `reserved` - Reservado
- `completed` - Concluído (inquilino encontrado)
- `cancelled` - Cancelado

**Funcionalidades de Anúncios:**
- ✅ Criar rascunhos sem seller/location (validação condicional)
- ✅ Publicar apenas anúncios completos
- ✅ Atualizar timestamp ao republicar (updated_at renovado)
- ✅ Alterar status do anúncio (endpoint PATCH /api/ads/{id}/status)

### Upload de Imagens
- `POST /api/upload/image` - Upload de imagem 🔒
  - Máximo 15 imagens por anúncio
  - Tamanho máximo: 5MB por imagem
  - Formatos: JPG, JPEG, PNG, WEBP

### Comentários
- `GET /api/comments/ad/{ad_id}` - Comentários de um anúncio
- `GET /api/comments/{id}` - Detalhes do comentário
- `POST /api/comments` - Criar comentário 🔒
- `PUT /api/comments/{id}` - Atualizar comentário 🔒
- `DELETE /api/comments/{id}` - Deletar comentário 🔒

### Favoritos

---

## 🏛️ Arquitetura Clean Architecture

O projeto foi refatorado seguindo os princípios da Clean Architecture e SOLID:

```
app/
├── domain/                    # 🏛️ Camada de Domínio
│   ├── entities/
│   │   ├── ad.py             # Entidade Ad com regras de negócio
│   │   ├── user.py           # Entidade User
│   │   └── comment.py        # Entidade Comment
│   └── repositories/
│       ├── ad_repository.py  # Interface IAdRepository
│       ├── user_repository.py
│       └── comment_repository.py
│
├── application/               # 📋 Camada de Aplicação
│   ├── services/
│   │   ├── ad_service.py     # Lógica de negócio de anúncios
│   │   ├── user_service.py   # Lógica de negócio de usuários
│   │   └── comment_service.py
│   └── use_cases/             # Casos de uso específicos
│
├── infrastructure/            # 🔧 Camada de Infraestrutura
│   └── repositories/
│       ├── sqlalchemy_ad_repository.py
│       ├── sqlalchemy_user_repository.py
│       └── sqlalchemy_comment_repository.py
│
├── presentation/              # 🎨 Camada de Apresentação
│   └── routers/
│       ├── ads_refactored.py  # Endpoints refatorados
│       └── dependencies.py    # Injeção de dependências
│
├── core/                      # ⚙️ Configurações e Utilidades
│   ├── config.py
│   ├── security.py           # Autenticação JWT + bcrypt
│   └── exceptions.py         # Exceções customizadas
│
└── db/                        # 💾 Banco de Dados
    ├── database.py
    └── models.py              # Modelos SQLAlchemy
```

### Princípios SOLID Aplicados

- **S**ingle Responsibility: Cada classe tem uma única responsabilidade
- **O**pen/Closed: Aberto para extensão, fechado para modificação
- **L**iskov Substitution: Interfaces implementadas corretamente
- **I**nterface Segregation: Interfaces específicas e coesas
- **D**ependency Inversion: Dependências invertidas via interfaces

### Endpoints Refatorados

Acesse os endpoints refatorados com Clean Architecture:

- `GET /api/ads-refactored/` - Listar anúncios (arquitetura limpa)
- `GET /api/ads-refactored/me` - Meus anúncios refatorados
- `GET /api/ads-refactored/{id}` - Detalhes do anúncio refatorado
- `POST /api/ads-refactored/` - Criar anúncio (arquitetura limpa)
- `PUT /api/ads-refactored/{id}` - Atualizar anúncio refatorado
- `DELETE /api/ads-refactored/{id}` - Deletar anúncio refatorado
- `PATCH /api/ads-refactored/{id}/status` - Alterar status (com republicação)

---

## 🔒 Segurança

### Autenticação Bcrypt

O sistema utiliza **bcrypt** direto (sem passlib) para máxima compatibilidade:

```python
# Hashing de senha
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Verificação
is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed)
```

### JWT Tokens

- **Algoritmo**: HS256
- **Expiração**: 7 dias (10080 minutos)
- **Payload**: user_id, email, exp

---

## 📝 Regras de Negócio

### Validação Condicional de Anúncios

- **Rascunhos (draft)**:
  - Campos `seller` e `location` são **opcionais**
  - Permite salvar anúncios incompletos
  - Não aparecem na listagem pública

- **Publicados (published)**:
  - Campos `seller` e `location` são **obrigatórios**
  - Validação automática retorna erro 422 se faltarem
  - Timestamp `updated_at` atualizado ao republicar

### Republicação de Anúncios

Quando um anúncio muda de status para `published`:
```python
if new_status == AdStatus.PUBLISHED:
    ad.updated_at = datetime.utcnow()  # Renova o timestamp
```

Isso garante que anúncios republicados apareçam como "recentes" na listagem.

🔒 = Requer autenticação (Bearer Token)
- `GET /api/favorites` - Meus favoritos 🔒
- `POST /api/favorites/{ad_id}/toggle` - Adicionar/remover favorito 🔒
- `DELETE /api/favorites/{ad_id}` - Remover favorito 🔒
- `GET /api/favorites/check/{ad_id}` - Verificar se está nos favoritos 🔒

🔒 = Requer autenticação (Bearer Token)

## 🗄️ Modelo de Dados

### User (Usuário)
- `id`: INTEGER (PK)
- `email`: VARCHAR (unique)
- `name`: VARCHAR
- `hashed_password`: VARCHAR
- `is_active`: BOOLEAN
- `created_at`: DATETIME

### Category (Categoria)
- `id`: INTEGER (PK)
- `name`: VARCHAR
- `slug`: VARCHAR (unique)
- `description`: VARCHAR
- `created_at`: DATETIME

### Ad (Anúncio)
- `id`: INTEGER (PK)
- `user_id`: INTEGER (FK -> User)
- `category_id`: INTEGER (FK -> Category)
- `title`: VARCHAR
- `description`: TEXT
- `seller`: VARCHAR
- `location`: VARCHAR
- `cep`: VARCHAR
- `price`: FLOAT
- `bedrooms`: INTEGER
- `bathrooms`: INTEGER
- `rules`: JSON
- `amenities`: JSON
- `custom_rules`: VARCHAR
- `custom_amenities`: VARCHAR
- `images`: JSON
- `status`: VARCHAR (draft/published)
- `created_at`: DATETIME
- `updated_at`: DATETIME

### Comment (Comentário)
- `id`: INTEGER (PK)
- `ad_id`: INTEGER (FK -> Ad)
- `user_id`: INTEGER (FK -> User)
- `content`: TEXT
- `rating`: INTEGER (1-5)
- `created_at`: DATETIME
- `updated_at`: DATETIME

### Favorites (Favoritos)
- Tabela de relacionamento N:N entre User e Ad
- `user_id`: INTEGER (PK, FK -> User)
- `ad_id`: INTEGER (PK, FK -> Ad)
- `created_at`: DATETIME

## 🧪 Testes

Para executar os testes (quando implementados):

```bash
pytest
```

## 📦 Estrutura do Projeto

```
Backend-FastAPI/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação FastAPI principal
│   ├── core/                # Configurações core
│   │   ├── config.py        # Configurações e variáveis de ambiente
│   │   └── security.py      # Funções de segurança (hash, JWT)
│   ├── db/                  # Banco de dados
│   │   ├── database.py      # Configuração SQLAlchemy
│   │   └── models.py        # Modelos do banco
│   ├── routers/             # Rotas da API
│   │   ├── auth.py          # Autenticação
│   │   ├── users.py         # Usuários
│   │   ├── categories.py    # Categorias
│   │   ├── ads.py           # Anúncios
│   │   ├── comments.py      # Comentários
│   │   └── favorites.py     # Favoritos
│   └── schemas/             # Schemas Pydantic (validação)
│       ├── user.py
│       ├── category.py
│       ├── ad.py
│       ├── comment.py
│       └── favorite.py
├── init_db.py               # Script de inicialização do BD
├── requirements.txt         # Dependências Python
├── .env.example             # Exemplo de variáveis de ambiente
├── .gitignore
└── README.md
```

## 🛠️ Tecnologias Utilizadas

- **FastAPI** 0.115.0 - Framework web moderno e rápido
- **Uvicorn** - Servidor ASGI de alta performance
- **SQLAlchemy** 2.0+ - ORM para Python
- **Pydantic** 2.0+ - Validação de dados
- **python-jose[cryptography]** - JWT tokens
- **passlib[bcrypt]** - Hash de senhas
- **python-multipart** - Upload de arquivos
- **SQLite** - Banco de dados

## 🔄 Migrações de Banco (Alembic)

Para usar Alembic para controlar as migrações:

### Instalar Alembic

```bash
pip install alembic
```

### Inicializar Alembic

```bash
alembic init alembic
```

### Configurar alembic.ini

Edite `alembic/env.py` e `alembic.ini` conforme necessário.

### Criar migração

```bash
alembic revision --autogenerate -m "Descrição da migração"
```

### Aplicar migrações

```bash
alembic upgrade head
```

## 📝 Notas Adicionais

- Por padrão, os tokens JWT expiram em 7 dias (10080 minutos)
- O banco de dados SQLite é criado automaticamente em `temvagaai.db`
- Em produção, considere usar PostgreSQL ao invés de SQLite
- Certifique-se de configurar CORS adequadamente para produção
- Sempre use HTTPS em produção

## 👥 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é parte do trabalho acadêmico da disciplina de Desenvolvimento Web.

### Desenvolvido por Eduardo Ribeiro com ❤️ e ☕

**[⬆ Voltar ao topo](#-frontend---tem-vaga-aí)**

</div>