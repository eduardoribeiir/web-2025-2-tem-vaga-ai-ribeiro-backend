"""Ad Service - Application layer business logic"""
from typing import List, Optional
from app.domain.entities.ad import Ad, AdStatus
from app.domain.repositories.ad_repository import IAdRepository
from app.core.exceptions import NotFoundException, ForbiddenException, BusinessRuleException


class AdService:
    """Service layer for Ad business logic - Single Responsibility Principle"""
    
    def __init__(self, ad_repository: IAdRepository):
        self._ad_repository = ad_repository
    
    async def get_ad(self, ad_id: int) -> Ad:
        """Get ad by ID"""
        ad = await self._ad_repository.get_by_id(ad_id)
        if not ad:
            raise NotFoundException(f"Ad with ID {ad_id} not found")
        return ad
    
    async def list_ads(
        self,
        skip: int = 0,
        limit: int = 20,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        location: Optional[str] = None,
        bedrooms: Optional[int] = None,
        status: Optional[AdStatus] = AdStatus.PUBLISHED
    ) -> List[Ad]:
        """List ads with filters"""
        return await self._ad_repository.get_all(
            skip=skip,
            limit=limit,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            location=location,
            bedrooms=bedrooms,
            status=status
        )
    
    async def list_user_ads(self, user_id: int) -> List[Ad]:
        """List all ads from a user"""
        return await self._ad_repository.get_by_user(user_id)
    
    async def create_ad(self, ad: Ad, category_exists: bool) -> Ad:
        """Create new ad with validation
        
        If status is 'published', seller and location are required.
        For drafts, these fields are optional.
        """
        if not category_exists:
            raise NotFoundException(f"Category with ID {ad.category_id} not found")
        
        # Validate required fields for published ads
        if ad.status == AdStatus.PUBLISHED:
            if not ad.seller or not ad.seller.strip():
                raise BusinessRuleException("Campo 'seller' é obrigatório para anúncios publicados")
            if not ad.location or not ad.location.strip():
                raise BusinessRuleException("Campo 'location' é obrigatório para anúncios publicados")
        
        return await self._ad_repository.create(ad)
    
    async def update_ad(
        self,
        ad_id: int,
        updates: dict,
        current_user_id: int,
        category_exists: bool = True
    ) -> Ad:
        """Update ad with ownership and validation checks"""
        # Get existing ad
        ad = await self.get_ad(ad_id)
        
        # Check ownership
        if not ad.is_owned_by(current_user_id):
            raise ForbiddenException("You don't have permission to edit this ad")
        
        # Validate category if being updated
        if "category_id" in updates and not category_exists:
            raise NotFoundException(f"Category with ID {updates['category_id']} not found")
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(ad, key) and value is not None:
                setattr(ad, key, value)
        
        return await self._ad_repository.update(ad)
    
    async def delete_ad(self, ad_id: int, current_user_id: int) -> None:
        """Delete ad with ownership check"""
        ad = await self.get_ad(ad_id)
        
        if not ad.is_owned_by(current_user_id):
            raise ForbiddenException("You don't have permission to delete this ad")
        
        await self._ad_repository.delete(ad_id)
    
    async def change_ad_status(
        self,
        ad_id: int,
        new_status: AdStatus,
        current_user_id: int
    ) -> Ad:
        """Change ad status with validation
        
        When republishing (status -> published), updates the timestamp
        to reflect the new availability date
        """
        ad = await self.get_ad(ad_id)
        
        # Check ownership
        if not ad.is_owned_by(current_user_id):
            raise ForbiddenException("You don't have permission to change this ad's status")
        
        # Validate transition
        try:
            ad.change_status(new_status)
        except ValueError as e:
            raise BusinessRuleException(str(e))
        
        # When republishing, renew the timestamp (like a new ad)
        # This is important for vacancy systems where the same space
        # becomes available again after someone moves out
        if new_status == AdStatus.PUBLISHED:
            from datetime import datetime
            ad.updated_at = datetime.utcnow()
            ad.published_at = datetime.utcnow()  # Marca nova data de publicação
        
        return await self._ad_repository.update(ad)
