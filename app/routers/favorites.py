from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import models
from app.schemas import favorite as schemas
from app.schemas.ad import AdRead
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[AdRead])
async def get_my_favorites(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista anúncios favoritados pelo usuário autenticado"""
    # Busca anúncios favoritados através da relação many-to-many
    favorites = db.query(models.Ad).join(
        models.favorites_table,
        models.Ad.id == models.favorites_table.c.ad_id
    ).filter(
        models.favorites_table.c.user_id == current_user.id
    ).order_by(models.favorites_table.c.created_at.desc()).all()
    
    return [AdRead.model_validate(ad) for ad in favorites]

@router.post("/{ad_id}/toggle", response_model=schemas.FavoriteToggleResponse)
async def toggle_favorite(
    ad_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Adiciona ou remove anúncio dos favoritos (toggle)"""
    # Verifica se anúncio existe
    ad = db.query(models.Ad).filter(models.Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anúncio não encontrado"
        )
    
    # Verifica se já está nos favoritos
    is_favorited = db.query(models.favorites_table).filter(
        models.favorites_table.c.user_id == current_user.id,
        models.favorites_table.c.ad_id == ad_id
    ).first()
    
    if is_favorited:
        # Remove dos favoritos
        db.execute(
            models.favorites_table.delete().where(
                (models.favorites_table.c.user_id == current_user.id) &
                (models.favorites_table.c.ad_id == ad_id)
            )
        )
        db.commit()
        
        return schemas.FavoriteToggleResponse(
            favorited=False,
            message="Anúncio removido dos favoritos"
        )
    else:
        # Adiciona aos favoritos
        db.execute(
            models.favorites_table.insert().values(
                user_id=current_user.id,
                ad_id=ad_id
            )
        )
        db.commit()
        
        return schemas.FavoriteToggleResponse(
            favorited=True,
            message="Anúncio adicionado aos favoritos"
        )

@router.delete("/{ad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite(
    ad_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove anúncio dos favoritos"""
    # Verifica se está nos favoritos
    is_favorited = db.query(models.favorites_table).filter(
        models.favorites_table.c.user_id == current_user.id,
        models.favorites_table.c.ad_id == ad_id
    ).first()
    
    if not is_favorited:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anúncio não está nos favoritos"
        )
    
    # Remove dos favoritos
    db.execute(
        models.favorites_table.delete().where(
            (models.favorites_table.c.user_id == current_user.id) &
            (models.favorites_table.c.ad_id == ad_id)
        )
    )
    db.commit()
    
    return None

@router.get("/check/{ad_id}", response_model=bool)
async def check_is_favorited(
    ad_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Verifica se um anúncio está nos favoritos"""
    is_favorited = db.query(models.favorites_table).filter(
        models.favorites_table.c.user_id == current_user.id,
        models.favorites_table.c.ad_id == ad_id
    ).first()
    
    return is_favorited is not None
