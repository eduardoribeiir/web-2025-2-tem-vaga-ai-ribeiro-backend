# 🖥️ Backend - Tem Vaga Aí

<div align="center">

### _API RESTful robusta para gerenciamento de anúncios estudantis_

![Node.js](https://img.shields.io/badge/Node.js-18+-339933?logo=node.js&logoColor=white)
![Express](https://img.shields.io/badge/Express-5.0-000000?logo=express&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?logo=jsonwebtokens&logoColor=white)

</div>

---

## 📋 Sobre

API backend completa construída com **Node.js** e **Express**, oferecendo:

- 🔐 **Autenticação JWT** - Sistema seguro de login/registro
- 🏠 **CRUD de Anúncios** - Criação, leitura, atualização e exclusão
- 💾 **Sistema de Rascunhos** - Salve anúncios incompletos antes de publicar
- ❤️ **Gerenciamento de Favoritos** - Usuários podem marcar vagas favoritas
- 🗄️ **SQLite Integrado** - Banco de dados leve e sem configuração externa
- 🏗️ **Arquitetura em Camadas** - Código organizado e manutenível

---

## 🛠️ Stack Tecnológico

```javascript
{
  "runtime": "Node.js 18+",
  "framework": "Express 5",
  "database": "SQLite (better-sqlite3)",
  "auth": "JWT (jsonwebtoken)",
  "security": "bcryptjs (hash de senhas)",
  "env": "dotenv",
  "dev-tools": "nodemon"
}
```

---

## 📁 Estrutura do Projeto

```
backend/
├── src/
│   ├── config/
│   │   ├── db.js          # 🗄️ Configuração SQLite + migrations
│   │   └── env.js         # ⚙️ Variáveis de ambiente
│   ├── middleware/
│   │   ├── auth.js        # 🔒 Validação JWT
│   │   └── asyncHandler.js # 🛡️ Error handling
│   ├── modules/
│   │   ├── ads/           # 🏠 Anúncios (service + routes)
│   │   ├── auth/          # 🔐 Autenticação
│   │   ├── favorites/     # ❤️ Favoritos
│   │   └── users/         # 👤 Usuários
│   ├── routes/
│   │   └── index.js       # 🚦 Router principal
│   ├── utils/
│   │   ├── httpError.js   # ⚠️ Erros HTTP
│   │   └── token.js       # 🎟️ Geração JWT
│   ├── app.js             # 🚀 Express app
│   └── index.js           # 🎬 Entry point
├── .env.example           # 📝 Template variáveis de ambiente
├── package.json
└── README.md              # 📖 Você está aqui!
```

---

## 🚀 Instalação e Execução

### 1. Clone e entre no diretório

```bash
cd backend
```

### 2. Configure o ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite .env e defina:
# PORT=4000
# JWT_SECRET=seu-segredo-super-secreto-aqui
# DB_PATH=./database.sqlite (opcional, padrão já configurado)
```

### 3. Instale as dependências

```bash
npm install
```

### 4. Execute o servidor

**Modo Desenvolvimento** (com hot-reload):
```bash
npm run dev
```

**Modo Produção**:
```bash
npm start
```

✅ **Servidor rodando em:** `http://localhost:4000`

---

## 🧪 Testando a API

### Health Check

```bash
curl http://localhost:4000/health
# Resposta: {"status":"ok"}
```

### 1. Criar Conta

```bash
curl -X POST http://localhost:4000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria Silva",
    "email": "maria@example.com",
    "password": "senha123"
  }'
```

### 2. Fazer Login

```bash
curl -X POST http://localhost:4000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "maria@example.com",
    "password": "senha123"
  }'

# Guarde o token retornado!
```

### 3. Criar Anúncio

```bash
curl -X POST http://localhost:4000/api/ads \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Quarto em República Universitária",
    "description": "Quarto amplo, próximo à UFC",
    "seller": "Maria Silva",
    "location": "Centro",
    "category": "aluguel",
    "price": 450,
    "bedrooms": 1,
    "bathrooms": 1,
    "amenities": ["wifi", "ar-condicionado"],
    "status": "published"
  }'
```

### 4. Listar Anúncios Públicos

```bash
curl http://localhost:4000/api/ads
```

---

## 📡 Documentação da API

### 🔓 Rotas Públicas

#### `GET /health`
Retorna o status da API.

**Resposta:**
```json
{ "status": "ok" }
```

#### `POST /api/auth/register`
Cria nova conta de usuário.

**Body:**
```json
{
  "name": "string (opcional)",
  "email": "string (obrigatório)",
  "password": "string (obrigatório)"
}
```

**Resposta:**
```json
{
  "user": { "id": 1, "name": "...", "email": "..." },
  "token": "eyJhbGciOi..."
}
```

#### `POST /api/auth/login`
Autentica usuário existente.

**Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Resposta:** _(mesma do register)_

#### `GET /api/ads`
Lista todos os anúncios **publicados** (status = "published").

**Resposta:**
```json
[
  {
    "id": 1,
    "title": "...",
    "description": "...",
    "price": 450,
    "location": "...",
    "category": "aluguel",
    "bedrooms": 1,
    "bathrooms": 1,
    "amenities": ["wifi"],
    "images": [],
    "status": "published"
  }
]
```

#### `GET /api/ads/:id`
Retorna detalhes de um anúncio específico.

---

### 🔒 Rotas Autenticadas

> **Atenção:** Todas as rotas abaixo requerem header `Authorization: Bearer <token>`

#### `POST /api/ads`
Cria novo anúncio.

**Campos obrigatórios:**
- `title` (string)
- `description` (string)
- `seller` (string)
- `location` (string)
- `category` (string: "aluguel", "venda", "serviço", "outro")

**Campos opcionais:**
- `cep` (string)
- `price` (number)
- `bedrooms` (number)
- `bathrooms` (number)
- `rules` (array de strings)
- `amenities` (array de strings)
- `custom_rules` (string)
- `custom_amenities` (string)
- `images` (array de URLs)
- `status` ("draft" | "published", padrão: "published")

#### `PUT /api/ads/:id`
Atualiza anúncio existente (apenas do próprio usuário).

**Body:** _(aceita os mesmos campos do POST, todos opcionais)_

#### `DELETE /api/ads/:id`
Exclui anúncio (apenas do próprio usuário).

#### `GET /api/users/me/ads`
Lista todos os anúncios do usuário autenticado (incluindo rascunhos).

#### `GET /api/favorites`
Lista favoritos do usuário autenticado.

#### `POST /api/favorites/:adId/toggle`
Adiciona ou remove anúncio dos favoritos.

**Resposta:**
```json
{ "favorite": true }  // ou false se removeu
```

---

## 🗄️ Banco de Dados

O SQLite cria automaticamente as seguintes tabelas:

### `users`
| Campo | Tipo | Descrição |
|-------|------|----------|
| id | INTEGER | Primary key |
| name | TEXT | Nome do usuário |
| email | TEXT | Email (unique) |
| password_hash | TEXT | Hash bcrypt da senha |
| created_at | DATETIME | Data de criação |

### `ads`
| Campo | Tipo | Descrição |
|-------|------|----------|
| id | INTEGER | Primary key |
| user_id | INTEGER | FK → users |
| title | TEXT | Título do anúncio |
| description | TEXT | Descrição |
| seller | TEXT | Nome do anunciante |
| location | TEXT | Localização |
| cep | TEXT | CEP |
| price | REAL | Preço |
| category | TEXT | Categoria |
| bedrooms | INTEGER | Nº quartos |
| bathrooms | INTEGER | Nº banheiros |
| rules | TEXT | Regras (JSON array) |
| amenities | TEXT | Comodidades (JSON array) |
| custom_rules | TEXT | Regras personalizadas |
| custom_amenities | TEXT | Comodidades personalizadas |
| images | TEXT | URLs imagens (JSON array) |
| status | TEXT | "draft" ou "published" |
| created_at | DATETIME | Data criação |
| updated_at | DATETIME | Data atualização |

### `favorites`
| Campo | Tipo | Descrição |
|-------|------|----------|
| user_id | INTEGER | FK → users |
| ad_id | INTEGER | FK → ads |
| created_at | DATETIME | Data |
| **PK** | (user_id, ad_id) | Chave composta |

---

## 🔒 Segurança

- ✅ Senhas são hasheadas com **bcrypt** (salt rounds: 10)
- ✅ Tokens JWT expiram em **7 dias**
- ✅ Middleware de autenticação valida tokens em todas as rotas protegidas
- ✅ SQLite usa prepared statements (proteção contra SQL injection)
- ✅ CORS habilitado para integração com frontend

---

## 📝 Scripts Disponíveis

```bash
npm run dev     # Modo desenvolvimento (nodemon com hot-reload)
npm start       # Modo produção (node puro)
```

---

## 🐛 Troubleshooting

**Erro: "Port 4000 already in use"**
```bash
# Windows
taskkill /IM node.exe /F

# Linux/Mac
lsof -ti:4000 | xargs kill -9
```

**Erro: "JWT_SECRET not defined"**
- Verifique se o arquivo `.env` existe e contém `JWT_SECRET=alguma-chave`

**Banco não cria tabelas**
- Delete `database.sqlite` e reinicie o servidor
- As migrations rodam automaticamente no startup

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Antes de abrir um PR:

1. Teste localmente com `npm run dev`
2. Verifique se não quebrou endpoints existentes
3. Documente novas rotas neste README

---

<div align="center">

### Desenvolvido com ☕ e 💻

**[⬆ Voltar ao topo](#️-backend---tem-vaga-aí)**

</div>
