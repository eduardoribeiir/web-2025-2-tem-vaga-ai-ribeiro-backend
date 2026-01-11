"""
Ads Router - Refactored following Clean Architecture
- Thin controllers
- Delegates to service layer
- Handles only HTTP concerns
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.db import models
from app.schemas import ad as schemas
from app.routers.auth import get_current_user
from app.core.dependencies import get_service_container
from app.core.exceptions import (
    NotFoundException,
    ForbiddenException,
    BusinessRuleException
)
from app.domain.entities.ad import Ad as DomainAd, AdStatus

router = APIRouter()


def _map_exception_to_http(e: Exception) -> HTTPException:
    """Map domain exceptions to HTTP exceptions"""
    if isinstance(e, NotFoundException):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    elif isinstance(e, ForbiddenException):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    elif isinstance(e, BusinessRuleException):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    elif isinstance(e, ValueError):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=List[schemas.AdRead])
async def get_ads(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    location: Optional[str] = None,
    bedrooms: Optional[int] = None,
    status_param: Optional[schemas.AdStatus] = Query(schemas.AdStatus.PUBLISHED, alias="status"),
    db: Session = Depends(get_db)
):
    """List ads with filters - Delegates to service layer"""
    try:
        container = get_service_container(db)
        ad_service = container.get_ad_service()
        
        # Convert schema enum to domain enum
        domain_status = AdStatus(status_param.value) if status_param else None
        
        # Call service
        domain_ads = await ad_service.list_ads(
            skip=skip,
            limit=limit,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            location=location,
            bedrooms=bedrooms,
            status=domain_status
        )
        
        # Convert domain entities to schemas (presentation layer concern)
        return [_domain_ad_to_schema(ad) for ad in domain_ads]
    
    except Exception as e:
        raise _map_exception_to_http(e)


@router.get("/me", response_model=List[schemas.AdRead])
async def get_my_ads(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List current user's ads"""
    try:
        container = get_service_container(db)
        ad_service = container.get_ad_service()
        
        domain_ads = await ad_service.list_user_ads(current_user.id)
        return [_domain_ad_to_schema(ad) for ad in domain_ads]
    
    except Exception as e:
        raise _map_exception_to_http(e)


@router.get("/{ad_id}", response_model=schemas.AdReadWithOwner)
async def get_ad(
    ad_id: int,
    db: Session = Depends(get_db)
):
    """Get ad by ID with owner information"""
    try:
        container = get_service_container(db)
        ad_service = container.get_ad_service()
        
        domain_ad = await ad_service.get_ad(ad_id)
        
        # Get owner info from database (for now, still coupled to DB)
        # TODO: Move to service layer
        ad_orm = db.query(models.Ad).filter(models.Ad.id == ad_id).first()
        
        return schemas.AdReadWithOwner.model_validate(ad_orm)
    
    except Exception as e:
        raise _map_exception_to_http(e)


@router.post("/", response_model=schemas.AdRead, status_code=status.HTTP_201_CREATED)
async def create_ad(
    ad_data: schemas.AdCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new ad"""
    try:
        container = get_service_container(db)
        ad_service = container.get_ad_service()
        
        # Check if category exists (still coupled to DB - TODO: move to service)
        category_exists = db.query(models.Category).filter(
            models.Category.id == ad_data.category_id
        ).first() is not None
        
        # Convert schema to domain entity
        domain_ad = DomainAd(
            title=ad_data.title,
            description=ad_data.description,
            price=ad_data.price,
            category_id=ad_data.category_id,
            user_id=current_user.id,
            seller=ad_data.seller,
            location=ad_data.location,
            cep=ad_data.cep,
            bedrooms=ad_data.bedrooms,
            bathrooms=ad_data.bathrooms,
            rules=ad_data.rules or [],
            amenities=ad_data.amenities or [],
            custom_rules=ad_data.custom_rules,
            custom_amenities=ad_data.custom_amenities,
            images=ad_data.images or [],
            status=AdStatus(ad_data.status) if ad_data.status else AdStatus.PUBLISHED
        )
        
        # Call service
        created_ad = await ad_service.create_ad(domain_ad, category_exists)
        
        return _domain_ad_to_schema(created_ad)
    
    except Exception as e:
        raise _map_exception_to_http(e)


@router.put("/{ad_id}", response_model=schemas.AdRead)
async def update_ad(
    ad_id: int,
    ad_data: schemas.AdUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update ad - Only owner can update"""
    try:
        container = get_service_container(db)
        ad_service = container.get_ad_service()
        
        # Check category if provided
        category_exists = True
        if ad_data.category_id:
            category_exists = db.query(models.Category).filter(
                models.Category.id == ad_data.category_id
            ).first() is not None
        
        # Prepare updates dict
        updates = ad_data.model_dump(exclude_unset=True)
        
        # Call service
        updated_ad = await ad_service.update_ad(
            ad_id=ad_id,
            updates=updates,
            current_user_id=current_user.id,
            category_exists=category_exists
        )
        
        return _domain_ad_to_schema(updated_ad)
    
    except Exception as e:
        raise _map_exception_to_http(e)


@router.delete("/{ad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ad(
    ad_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete ad - Only owner can delete"""
    try:
        container = get_service_container(db)
        ad_service = container.get_ad_service()
        
        await ad_service.delete_ad(ad_id, current_user.id)
    
    except Exception as e:
        raise _map_exception_to_http(e)


@router.patch("/{ad_id}/status", response_model=schemas.AdRead)
async def change_ad_status(
    ad_id: int,
    new_status: schemas.AdStatus = Query(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change ad status - Only owner can change"""
    try:
        container = get_service_container(db)
        ad_service = container.get_ad_service()
        
        # Convert schema enum to domain enum
        domain_status = AdStatus(new_status.value)
        
        # Call service
        updated_ad = await ad_service.change_ad_status(
            ad_id=ad_id,
            new_status=domain_status,
            current_user_id=current_user.id
        )
        
        return _domain_ad_to_schema(updated_ad)
    
    except Exception as e:
        raise _map_exception_to_http(e)


def _domain_ad_to_schema(ad: DomainAd) -> schemas.AdRead:
    """Helper to convert domain entity to schema"""
    return schemas.AdRead(
        id=ad.id,
        title=ad.title,
        description=ad.description,
        seller=ad.seller,
        location=ad.location,
        cep=ad.cep,
        price=ad.price,
        category_id=ad.category_id,
        bedrooms=ad.bedrooms,
        bathrooms=ad.bathrooms,
        rules=ad.rules,
        amenities=ad.amenities,
        custom_rules=ad.custom_rules,
        custom_amenities=ad.custom_amenities,
        images=ad.images,
        status=schemas.AdStatus(ad.status.value),
        user_id=ad.user_id,
        created_at=ad.created_at,
        updated_at=ad.updated_at
    )
