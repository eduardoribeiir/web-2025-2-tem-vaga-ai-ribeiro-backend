"""Ad Repository Interface - Defines contract for ad persistence"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.ad import Ad, AdStatus


class IAdRepository(ABC):
    """Repository interface for Ad entity - Dependency Inversion Principle"""
    
    @abstractmethod
    async def get_by_id(self, ad_id: int) -> Optional[Ad]:
        """Get ad by ID"""
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    async def get_by_user(self, user_id: int) -> List[Ad]:
        """Get all ads from a user"""
        pass
    
    @abstractmethod
    async def create(self, ad: Ad) -> Ad:
        """Create new ad"""
        pass
    
    @abstractmethod
    async def update(self, ad: Ad) -> Ad:
        """Update existing ad"""
        pass
    
    @abstractmethod
    async def delete(self, ad_id: int) -> bool:
        """Delete ad"""
        pass
    
    @abstractmethod
    async def exists(self, ad_id: int) -> bool:
        """Check if ad exists"""
        pass
