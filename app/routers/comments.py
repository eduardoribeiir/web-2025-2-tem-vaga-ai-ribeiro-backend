from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import models
from app.schemas import comment as schemas
from app.routers.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/ad/{ad_id}", response_model=List[schemas.CommentReadWithUser])
async def get_ad_comments(ad_id: int, db: Session = Depends(get_db)):
    """Lista comentários de um anúncio"""
    # Verifica se anúncio existe
    ad = db.query(models.Ad).filter(models.Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anúncio não encontrado"
        )
    
    comments = db.query(models.Comment).filter(
        models.Comment.ad_id == ad_id
    ).order_by(models.Comment.created_at.desc()).all()
    
    return [schemas.CommentReadWithUser.model_validate(comment) for comment in comments]

@router.get("/{comment_id}", response_model=schemas.CommentReadWithUser)
async def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """Retorna um comentário específico"""
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentário não encontrado"
        )
    
    return schemas.CommentReadWithUser.model_validate(comment)

@router.post("/", response_model=schemas.CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: schemas.CommentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cria um novo comentário"""
    # Verifica se anúncio existe
    ad = db.query(models.Ad).filter(models.Ad.id == comment_data.ad_id).first()
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anúncio não encontrado"
        )
    
    # Cria comentário
    new_comment = models.Comment(
        **comment_data.model_dump(),
        user_id=current_user.id
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return schemas.CommentRead.model_validate(new_comment)

@router.put("/{comment_id}", response_model=schemas.CommentRead)
async def update_comment(
    comment_id: int,
    comment_data: schemas.CommentUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza um comentário (apenas o autor pode atualizar)"""
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentário não encontrado"
        )
    
    # Verifica se o usuário é o autor
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para editar este comentário"
        )
    
    # Atualiza campos
    update_data = comment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(comment, field, value)
    
    comment.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(comment)
    
    return schemas.CommentRead.model_validate(comment)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deleta um comentário (apenas o autor pode deletar)"""
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentário não encontrado"
        )
    
    # Verifica se o usuário é o autor
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para deletar este comentário"
        )
    
    db.delete(comment)
    db.commit()
    
    return None
