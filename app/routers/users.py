from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import models
from app.schemas import user as schemas
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/me", response_model=schemas.UserRead)
async def get_my_profile(current_user: models.User = Depends(get_current_user)):
    """Retorna perfil do usuário autenticado"""
    return schemas.UserRead.model_validate(current_user)

@router.put("/me", response_model=schemas.UserRead)
async def update_my_profile(
    user_data: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza perfil do usuário autenticado"""
    # Verifica se email já está em uso por outro usuário
    if user_data.email and user_data.email != current_user.email:
        existing_user = db.query(models.User).filter(
            models.User.email == user_data.email,
            models.User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email já está em uso"
            )
    
    # Atualiza campos
    if user_data.name is not None:
        current_user.name = user_data.name
    if user_data.email is not None:
        current_user.email = user_data.email
    
    db.commit()
    db.refresh(current_user)
    
    return schemas.UserRead.model_validate(current_user)

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_account(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deleta conta do usuário autenticado"""
    # Deleta anúncios do usuário
    db.query(models.Ad).filter(models.Ad.user_id == current_user.id).delete()
    
    # Deleta comentários do usuário
    db.query(models.Comment).filter(models.Comment.user_id == current_user.id).delete()
    
    # Deleta favoritos do usuário
    db.execute(
        models.favorites_table.delete().where(
            models.favorites_table.c.user_id == current_user.id
        )
    )
    
    # Deleta usuário
    db.delete(current_user)
    db.commit()
    
    return None

@router.get("/{user_id}", response_model=schemas.UserRead)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Retorna informações públicas de um usuário"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return schemas.UserRead.model_validate(user)
