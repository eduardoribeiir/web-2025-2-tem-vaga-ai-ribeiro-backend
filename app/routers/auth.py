from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas import user as schemas
from app.core import security
from datetime import timedelta
from app.core.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """Dependency para obter usuário autenticado"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = security.decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: int = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

@router.post("/register", response_model=schemas.AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário"""
    # Verifica se email já existe
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado"
        )
    
    # Cria usuário
    hashed_password = security.get_password_hash(user_data.password)
    new_user = models.User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Gera token
    access_token = security.create_access_token(
        data={"user_id": new_user.id, "email": new_user.email}
    )
    
    return schemas.AuthResponse(
        user=schemas.UserRead.model_validate(new_user),
        token=schemas.Token(access_token=access_token, token_type="bearer")
    )

@router.post("/login", response_model=schemas.AuthResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Autentica um usuário e retorna token JWT"""
    # Busca usuário
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Gera token
    access_token = security.create_access_token(
        data={"user_id": user.id, "email": user.email}
    )
    
    return schemas.AuthResponse(
        user=schemas.UserRead.model_validate(user),
        token=schemas.Token(access_token=access_token, token_type="bearer")
    )

@router.post("/login/json", response_model=schemas.AuthResponse)
async def login_json(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """Autentica um usuário via JSON (alternativa ao form)"""
    # Busca usuário
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user or not security.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    # Gera token
    access_token = security.create_access_token(
        data={"user_id": user.id, "email": user.email}
    )
    
    return schemas.AuthResponse(
        user=schemas.UserRead.model_validate(user),
        token=schemas.Token(access_token=access_token, token_type="bearer")
    )

@router.get("/me", response_model=schemas.UserRead)
async def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    """Retorna informações do usuário autenticado"""
    return schemas.UserRead.model_validate(current_user)
