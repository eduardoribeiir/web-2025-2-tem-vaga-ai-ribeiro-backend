# ⚡ Quick Start - TemVagaAi Backend FastAPI

Guia rápido para executar o backend em **5 minutos**!

## 🎯 Passos Rápidos

### 1️⃣ Crie o ambiente virtual e instale dependências

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2️⃣ Configure o arquivo .env

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

**⚠️ Edite `.env` e altere o SECRET_KEY:**

```env
SECRET_KEY=sua-chave-segura-aqui
```

Para gerar uma chave segura:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3️⃣ Inicialize o banco de dados

```bash
python init_db.py
```

Isso irá criar:
- ✅ Tabelas no banco de dados
- ✅ 5 categorias padrão
- ✅ Usuário de teste: `teste@temvagaai.com` / `senha123`
- ✅ 2 anúncios de exemplo

### 4️⃣ Execute o servidor

```bash
uvicorn app.main:app --reload
```

🎉 **Pronto!** A API está rodando em: http://localhost:8000

## 📚 Próximos Passos

### Acesse a documentação interativa:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Teste a API com o script de testes:
```bash
python test_api.py
```

### Teste manualmente com cURL:

**1. Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=teste@temvagaai.com&password=senha123"
```

**2. Listar anúncios:**
```bash
curl "http://localhost:8000/api/v1/ads"
```

**3. Listar categorias:**
```bash
curl "http://localhost:8000/api/v1/categories"
```

## 🔧 Comandos Úteis

### Parar o servidor
Pressione `Ctrl+C` no terminal

### Recriar o banco de dados
```bash
# Delete o arquivo do banco
rm temvagaai.db  # Linux/Mac
del temvagaai.db  # Windows

# Recrie
python init_db.py
```

### Desativar ambiente virtual
```bash
deactivate
```

## 📝 Credenciais de Teste

- **Email:** teste@temvagaai.com
- **Senha:** senha123

## ❓ Problemas Comuns

### Erro: "No module named 'app'"
- Certifique-se de estar na pasta `Backend-FastAPI`
- Certifique-se de ter ativado o ambiente virtual

### Erro: "uvicorn: command not found"
- Execute: `pip install -r requirements.txt`

### Erro ao executar init_db.py
- Delete o arquivo `temvagaai.db` se existir
- Execute novamente: `python init_db.py`

## 🚀 Para Produção

1. Configure um banco PostgreSQL
2. Altere `DATABASE_URL` no `.env`
3. Gere nova SECRET_KEY segura
4. Configure CORS adequadamente
5. Use servidor ASGI de produção (Gunicorn + Uvicorn)
6. Use HTTPS

---

**Pronto para desenvolver! 🎉**

Para mais informações, veja [README.md](README.md)
