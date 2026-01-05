# TemVagaAi - Backend FastAPI

Backend da aplicação TemVagaAi desenvolvido com FastAPI, SQLAlchemy e SQLite.

## 📋 Pré-requisitos

- Python 3.10 ou superior
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

### Modo desenvolvimento (com auto-reload)

```bash
uvicorn app.main:app --reload
```

### Modo produção

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
- `POST /api/v1/auth/register` - Registrar novo usuário
- `POST /api/v1/auth/login` - Login (OAuth2 form)
- `POST /api/v1/auth/login/json` - Login (JSON)
- `GET /api/v1/auth/me` - Informações do usuário autenticado

### Usuários
- `GET /api/v1/users/me` - Perfil do usuário autenticado
- `PUT /api/v1/users/me` - Atualizar perfil
- `DELETE /api/v1/users/me` - Deletar conta
- `GET /api/v1/users/{user_id}` - Informações públicas de um usuário

### Categorias
- `GET /api/v1/categories` - Listar categorias
- `GET /api/v1/categories/{id}` - Detalhes da categoria
- `POST /api/v1/categories` - Criar categoria 🔒
- `PUT /api/v1/categories/{id}` - Atualizar categoria 🔒
- `DELETE /api/v1/categories/{id}` - Deletar categoria 🔒

### Anúncios
- `GET /api/v1/ads` - Listar anúncios (com filtros)
- `GET /api/v1/ads/{id}` - Detalhes do anúncio
- `GET /api/v1/ads/me` - Meus anúncios 🔒
- `POST /api/v1/ads` - Criar anúncio 🔒
- `PUT /api/v1/ads/{id}` - Atualizar anúncio 🔒
- `DELETE /api/v1/ads/{id}` - Deletar anúncio 🔒

### Comentários
- `GET /api/v1/comments/ad/{ad_id}` - Comentários de um anúncio
- `GET /api/v1/comments/{id}` - Detalhes do comentário
- `POST /api/v1/comments` - Criar comentário 🔒
- `PUT /api/v1/comments/{id}` - Atualizar comentário 🔒
- `DELETE /api/v1/comments/{id}` - Deletar comentário 🔒

### Favoritos
- `GET /api/v1/favorites` - Meus favoritos 🔒
- `POST /api/v1/favorites/{ad_id}/toggle` - Adicionar/remover favorito 🔒
- `DELETE /api/v1/favorites/{ad_id}` - Remover favorito 🔒
- `GET /api/v1/favorites/check/{ad_id}` - Verificar se está nos favoritos 🔒

🔒 = Requer autenticação

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
