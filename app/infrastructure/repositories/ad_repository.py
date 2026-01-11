"""SQLAlchemy Ad Repository Implementation"""
import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.ad import Ad, AdStatus
from app.domain.repositories.ad_repository import IAdRepository
from app.db import models


class SQLAlchemyAdRepository(IAdRepository):
    """Concrete implementation of Ad Repository using SQLAlchemy"""
    
    def __init__(self, db: Session):
        self._db = db
    
    def _to_domain(self, db_ad: models.Ad) -> Ad:
        """Convert ORM model to domain entity"""
        return Ad(
            id=db_ad.id,
            title=db_ad.title,
            description=db_ad.description,
            price=db_ad.price,
            category_id=db_ad.category_id,
            user_id=db_ad.user_id,
            seller=db_ad.seller,
            location=db_ad.location,
            cep=db_ad.cep,
            bedrooms=db_ad.bedrooms,
            bathrooms=db_ad.bathrooms,
            rules=json.loads(db_ad.rules) if db_ad.rules else [],
            amenities=json.loads(db_ad.amenities) if db_ad.amenities else [],
            custom_rules=db_ad.custom_rules,
            custom_amenities=db_ad.custom_amenities,
            images=json.loads(db_ad.images) if db_ad.images else [],
            status=AdStatus(db_ad.status),
            created_at=db_ad.created_at,
            updated_at=db_ad.updated_at,
            published_at=db_ad.published_at
        )
    
    def _to_orm(self, ad: Ad) -> models.Ad:
        """Convert domain entity to ORM model"""
        return models.Ad(
            id=ad.id,
            title=ad.title,
            description=ad.description,
            price=ad.price,
            category_id=ad.category_id,
            user_id=ad.user_id,
            seller=ad.seller,
            location=ad.location,
            cep=ad.cep,
            bedrooms=ad.bedrooms,
            bathrooms=ad.bathrooms,
            rules=json.dumps(ad.rules) if ad.rules else None,
            amenities=json.dumps(ad.amenities) if ad.amenities else None,
            custom_rules=ad.custom_rules,
            custom_amenities=ad.custom_amenities,
            images=json.dumps(ad.images) if ad.images else None,
            status=ad.status.value,
            published_at=ad.published_at
        )
    
    async def get_by_id(self, ad_id: int) -> Optional[Ad]:
        """Get ad by ID"""
        db_ad = self._db.query(models.Ad).filter(models.Ad.id == ad_id).first()
        return self._to_domain(db_ad) if db_ad else None
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        location: Optional[str] = None,
        bedrooms: Optional[int] = None,
        status: Optional[AdStatus] = None
    ) -> List[Ad]:
        """Get ads with filters"""
        query = self._db.query(models.Ad)
        
        # Apply filters
        if status:
            query = query.filter(models.Ad.status == status.value)
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
        
        # Order and paginate
        query = query.order_by(models.Ad.created_at.desc())
        db_ads = query.offset(skip).limit(limit).all()
        
        return [self._to_domain(ad) for ad in db_ads]
    
    async def get_by_user(self, user_id: int) -> List[Ad]:
        """Get all ads from a user"""
        db_ads = self._db.query(models.Ad).filter(
            models.Ad.user_id == user_id
        ).order_by(models.Ad.created_at.desc()).all()
        
        return [self._to_domain(ad) for ad in db_ads]
    
    async def create(self, ad: Ad) -> Ad:
        """Create new ad"""
        db_ad = self._to_orm(ad)
        self._db.add(db_ad)
        self._db.commit()
        self._db.refresh(db_ad)
        return self._to_domain(db_ad)
    
    async def update(self, ad: Ad) -> Ad:
        """Update existing ad"""
        db_ad = self._db.query(models.Ad).filter(models.Ad.id == ad.id).first()
        if db_ad:
            # Update fields
            db_ad.title = ad.title
            db_ad.description = ad.description
            db_ad.price = ad.price
            db_ad.category_id = ad.category_id
            db_ad.seller = ad.seller
            db_ad.location = ad.location
            db_ad.cep = ad.cep
            db_ad.bedrooms = ad.bedrooms
            db_ad.bathrooms = ad.bathrooms
            db_ad.rules = json.dumps(ad.rules) if ad.rules else None
            db_ad.amenities = json.dumps(ad.amenities) if ad.amenities else None
            db_ad.custom_rules = ad.custom_rules
            db_ad.custom_amenities = ad.custom_amenities
            db_ad.images = json.dumps(ad.images) if ad.images else None
            db_ad.status = ad.status.value
            
            self._db.commit()
            self._db.refresh(db_ad)
            return self._to_domain(db_ad)
        return ad
    
    async def delete(self, ad_id: int) -> bool:
        """Delete ad"""
        db_ad = self._db.query(models.Ad).filter(models.Ad.id == ad_id).first()
        if db_ad:
            self._db.delete(db_ad)
            self._db.commit()
            return True
        return False
    
    async def exists(self, ad_id: int) -> bool:
        """Check if ad exists"""
        return self._db.query(models.Ad).filter(models.Ad.id == ad_id).first() is not None
