from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.db import models
from app.schemas import category as schemas
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.CategoryRead])
async def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista todas as categorias"""
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return [schemas.CategoryRead.model_validate(cat) for cat in categories]

@router.get("/{category_id}", response_model=schemas.CategoryRead)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    """Retorna uma categoria específica"""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )
    
    return schemas.CategoryRead.model_validate(category)

@router.post("/", response_model=schemas.CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: schemas.CategoryCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cria uma nova categoria (requer autenticação)"""
    # Verifica se slug já existe
    existing = db.query(models.Category).filter(
        models.Category.slug == category_data.slug
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slug já está em uso"
        )
    
    new_category = models.Category(**category_data.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return schemas.CategoryRead.model_validate(new_category)

@router.put("/{category_id}", response_model=schemas.CategoryRead)
async def update_category(
    category_id: int,
    category_data: schemas.CategoryUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza uma categoria (requer autenticação)"""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )
    
    # Verifica se novo slug já existe
    if category_data.slug and category_data.slug != category.slug:
        existing = db.query(models.Category).filter(
            models.Category.slug == category_data.slug,
            models.Category.id != category_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Slug já está em uso"
            )
    
    # Atualiza campos
    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    return schemas.CategoryRead.model_validate(category)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deleta uma categoria (requer autenticação)"""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )
    
    # Verifica se há anúncios usando esta categoria
    ads_count = db.query(models.Ad).filter(models.Ad.category_id == category_id).count()
    if ads_count > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Não é possível deletar. Existem {ads_count} anúncios usando esta categoria"
        )
    
    db.delete(category)
    db.commit()
    
    return None
