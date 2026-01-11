"""Comment Repository Interface"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.comment import Comment


class ICommentRepository(ABC):
    """Repository interface for Comment entity"""
    
    @abstractmethod
    async def get_by_id(self, comment_id: int) -> Optional[Comment]:
        """Get comment by ID"""
        pass
    
    @abstractmethod
    async def get_by_ad(self, ad_id: int) -> List[Comment]:
        """Get all comments for an ad"""
        pass
    
    @abstractmethod
    async def create(self, comment: Comment) -> Comment:
        """Create new comment"""
        pass
    
    @abstractmethod
    async def update(self, comment: Comment) -> Comment:
        """Update comment"""
        pass
    
    @abstractmethod
    async def delete(self, comment_id: int) -> bool:
        """Delete comment"""
        pass
