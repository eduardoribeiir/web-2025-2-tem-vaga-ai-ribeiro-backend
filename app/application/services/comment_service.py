"""Comment Service - Comment business logic"""
from typing import List
from app.domain.entities.comment import Comment
from app.domain.repositories.comment_repository import ICommentRepository
from app.domain.repositories.ad_repository import IAdRepository
from app.core.exceptions import NotFoundException, ForbiddenException


class CommentService:
    """Service layer for Comment business logic"""
    
    def __init__(
        self,
        comment_repository: ICommentRepository,
        ad_repository: IAdRepository
    ):
        self._comment_repository = comment_repository
        self._ad_repository = ad_repository
    
    async def get_comment(self, comment_id: int) -> Comment:
        """Get comment by ID"""
        comment = await self._comment_repository.get_by_id(comment_id)
        if not comment:
            raise NotFoundException(f"Comment with ID {comment_id} not found")
        return comment
    
    async def list_ad_comments(self, ad_id: int) -> List[Comment]:
        """List all comments for an ad"""
        # Verify ad exists
        if not await self._ad_repository.exists(ad_id):
            raise NotFoundException(f"Ad with ID {ad_id} not found")
        
        return await self._comment_repository.get_by_ad(ad_id)
    
    async def create_comment(self, comment: Comment) -> Comment:
        """Create new comment"""
        # Verify ad exists
        if not await self._ad_repository.exists(comment.ad_id):
            raise NotFoundException(f"Ad with ID {comment.ad_id} not found")
        
        return await self._comment_repository.create(comment)
    
    async def update_comment(
        self,
        comment_id: int,
        updates: dict,
        current_user_id: int
    ) -> Comment:
        """Update comment with ownership check"""
        comment = await self.get_comment(comment_id)
        
        # Check ownership
        if not comment.is_owned_by(current_user_id):
            raise ForbiddenException("You don't have permission to edit this comment")
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(comment, key) and value is not None:
                setattr(comment, key, value)
        
        return await self._comment_repository.update(comment)
    
    async def delete_comment(self, comment_id: int, current_user_id: int) -> None:
        """Delete comment with ownership check"""
        comment = await self.get_comment(comment_id)
        
        # Check ownership
        if not comment.is_owned_by(current_user_id):
            raise ForbiddenException("You don't have permission to delete this comment")
        
        await self._comment_repository.delete(comment_id)
