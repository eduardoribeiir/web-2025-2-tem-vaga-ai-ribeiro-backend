# API "Tem Vaga Aí" (backend)

Backend em Node.js/Express com SQLite, autenticação JWT, CRUD de anúncios (inclui rascunho/publicação) e favoritos. Estrutura em camadas em `src/` (config, middleware, módulos, rotas).

## Pré-requisitos
- Node.js 18+

## Configuração e execução
1) Copie o template de ambiente:
```
cp .env.example .env
```
2) Edite `.env` e defina `JWT_SECRET` (opcional: `PORT=4000`, `DB_PATH=./database.sqlite`).
3) Instale dependências:
```
npm install
```
4) Rode em desenvolvimento (nodemon):
```
npm run dev
```
   ou produção:
```
npm start
```

As tabelas (users, ads, favorites) são criadas automaticamente em SQLite.

## Endpoints principais
- `GET /health` — status
- `POST /api/auth/register` — `{ name?, email, password }`
- `POST /api/auth/login` — `{ email, password }`
- `GET /api/ads` — lista anúncios **publicados** (status = "published")
- `GET /api/ads/:id` — anúncio por id
- `POST /api/ads` — cria anúncio (auth). Obrigatórios: `title, description, seller, location, category`; opcionais: `cep, price, bedrooms, bathrooms, rules[], amenities[], custom_rules, custom_amenities, images[], status('draft'|'published')`
- `PUT /api/ads/:id` — atualiza anúncio (auth do dono). Aceita os mesmos campos, inclusive `status` para publicar/rascunho
- `DELETE /api/ads/:id` — remove anúncio (auth do dono)
- `GET /api/users/me/ads` — anúncios do usuário autenticado (inclui rascunhos e publicados)
- `GET /api/favorites` — favoritos do usuário autenticado
- `POST /api/favorites/:adId/toggle` — alterna favorito (auth)

## Notas
- Envie `Authorization: Bearer <token>` para rotas protegidas.
- `status` padrão é `published`; envie `draft` para salvar rascunho.
- `rules`, `amenities` e `images` são arrays (JSON). Campos numéricos aceitam null/vazio.
