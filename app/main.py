from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.db.database import engine
from app.db import models
from app.routers import auth, users, ads, favorites, categories, upload, comments
from app.routers import ads_refactored  # Router refatorado com Clean Architecture
from pathlib import Path

# Criar tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos (uploads)
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Autenticação"])
app.include_router(users.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["Usuários"])
app.include_router(ads.router, prefix=f"{settings.API_V1_PREFIX}/ads", tags=["Anúncios"])
app.include_router(ads_refactored.router, prefix=f"{settings.API_V1_PREFIX}/ads-refactored", tags=["Anúncios Refatorados (Clean Architecture)"])
app.include_router(favorites.router, prefix=f"{settings.API_V1_PREFIX}/favorites", tags=["Favoritos"])
app.include_router(categories.router, prefix=f"{settings.API_V1_PREFIX}/categories", tags=["Categorias"])
app.include_router(upload.router, prefix=f"{settings.API_V1_PREFIX}/upload", tags=["Upload"])
app.include_router(comments.router, prefix=f"{settings.API_V1_PREFIX}/comments", tags=["Comentários"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Bem-vindo à API Tem Vaga Aí",
        "docs": "/docs",
        "version": "1.0.0"
    }
