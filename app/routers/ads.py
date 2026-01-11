from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import json
from app.db.database import get_db
from app.db import models
from app.schemas import ad as schemas
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.AdRead])
async def get_ads(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    location: Optional[str] = None,
    bedrooms: Optional[int] = None,
    status: Optional[schemas.AdStatus] = schemas.AdStatus.PUBLISHED,
    db: Session = Depends(get_db)
):
    """Lista anúncios com filtros opcionais"""
    query = db.query(models.Ad)
    
    # Filtros
    if status:
        query = query.filter(models.Ad.status == status)
    if category_id:
        query = query.filter(models.Ad.category_id == category_id)
    if min_price is not None:
        query = query.filter(models.Ad.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Ad.price <= max_price)
    if location:
        query = query.filter(models.Ad.location.ilike(f"%{location}%"))
    if bedrooms is not None:
        query = query.filter(models.Ad.bedrooms == bedrooms)
    
    # Ordena por data de criação (mais recentes primeiro)
    query = query.order_by(models.Ad.created_at.desc())
    
    ads = query.offset(skip).limit(limit).all()
    return [schemas.AdRead.model_validate(ad) for ad in ads]

@router.get("/me", response_model=List[schemas.AdRead])
async def get_my_ads(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista anúncios do usuário autenticado"""
    ads = db.query(models.Ad).filter(
        models.Ad.user_id == current_user.id
    ).order_by(models.Ad.created_at.desc()).all()
    
    return [schemas.AdRead.model_validate(ad) for ad in ads]

@router.get("/{ad_id}", response_model=schemas.AdReadWithOwner)
async def get_ad(ad_id: int, db: Session = Depends(get_db)):
    """Retorna um anúncio específico com informações do dono"""
    ad = db.query(models.Ad).filter(models.Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anúncio não encontrado"
        )
    
    return schemas.AdReadWithOwner.model_validate(ad)

@router.post("/", response_model=schemas.AdRead, status_code=status.HTTP_201_CREATED)
async def create_ad(
    ad_data: schemas.AdCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cria um novo anúncio
    
    Se status = 'published', os campos seller e location são obrigatórios.
    Para rascunhos (draft), esses campos são opcionais.
    """
    # Validação condicional: se for publicar, seller e location são obrigatórios
    if ad_data.status == schemas.AdStatus.PUBLISHED:
        if not ad_data.seller:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Campo 'seller' é obrigatório para anúncios publicados"
            )
        if not ad_data.location:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Campo 'location' é obrigatório para anúncios publicados"
            )
    
    # Verifica se categoria existe
    category = db.query(models.Category).filter(
        models.Category.id == ad_data.category_id
    ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )
    
    # Converte listas para JSON strings
    ad_dict = ad_data.model_dump()
    if ad_dict.get('rules'):
        ad_dict['rules'] = json.dumps(ad_dict['rules'])
    if ad_dict.get('amenities'):
        ad_dict['amenities'] = json.dumps(ad_dict['amenities'])
    if ad_dict.get('images'):
        ad_dict['images'] = json.dumps(ad_dict['images'])
    
    # Cria anúncio
    new_ad = models.Ad(**ad_dict, user_id=current_user.id)
    
    db.add(new_ad)
    db.commit()
    db.refresh(new_ad)
    
    return schemas.AdRead.model_validate(new_ad)

@router.put("/{ad_id}", response_model=schemas.AdRead)
async def update_ad(
    ad_id: int,
    ad_data: schemas.AdUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza um anúncio (apenas o dono pode atualizar)"""
    ad = db.query(models.Ad).filter(models.Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anúncio não encontrado"
        )
    
    # Verifica se o usuário é o dono
    if ad.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para editar este anúncio"
        )
    
    # Verifica categoria se fornecida
    if ad_data.category_id:
        category = db.query(models.Category).filter(
            models.Category.id == ad_data.category_id
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria não encontrada"
            )
    
    # Atualiza campos
    update_data = ad_data.model_dump(exclude_unset=True)
    
    # Converte listas para JSON strings
    if 'rules' in update_data and update_data['rules'] is not None:
        update_data['rules'] = json.dumps(update_data['rules'])
    if 'amenities' in update_data and update_data['amenities'] is not None:
        update_data['amenities'] = json.dumps(update_data['amenities'])
    if 'images' in update_data and update_data['images'] is not None:
        update_data['images'] = json.dumps(update_data['images'])
    
    for field, value in update_data.items():
        setattr(ad, field, value)
    
    ad.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(ad)
    
    return schemas.AdRead.model_validate(ad)

@router.delete("/{ad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ad(
    ad_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deleta um anúncio (apenas o dono pode deletar)"""
    ad = db.query(models.Ad).filter(models.Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anúncio não encontrado"
        )
    
    # Verifica se o usuário é o dono
    if ad.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para deletar este anúncio"
        )
    
    db.delete(ad)
    db.commit()
    
    return None

@router.patch("/{ad_id}/status", response_model=schemas.AdRead)
async def update_ad_status(
    ad_id: int,
    new_status: schemas.AdStatus,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza o status de um anúncio.
    Fluxo: draft → published → reserved → completed
    Apenas o dono pode mudar o status.
    """
    ad = db.query(models.Ad).filter(models.Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anúncio não encontrado"
        )
    
    # Verifica se o usuário é o dono
    if ad.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para alterar o status deste anúncio"
        )
    
    # Valida transições de status
    valid_transitions = {
        "draft": ["published", "cancelled"],
        "published": ["reserved", "cancelled"],
        "reserved": ["completed", "published"],
        "completed": [],
        "cancelled": ["draft", "published"]
    }
    
    current_status = ad.status
    if new_status not in valid_transitions.get(current_status, []):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Transição de status inválida: {current_status} → {new_status}"
        )
    
    # Atualiza status
    ad.status = new_status
    ad.updated_at = datetime.utcnow()
    
    # Quando republicar (voltar para published), atualiza a data de publicação
    # Isso é importante para sistemas de vagas onde o mesmo espaço
    # fica disponível novamente após alguém se mudar
    if new_status == "published":
        ad.published_at = datetime.utcnow()
    
    db.commit()
    db.refresh(ad)
    
    return schemas.AdRead.model_validate(ad)
