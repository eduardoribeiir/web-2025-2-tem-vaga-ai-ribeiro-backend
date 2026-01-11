"""SQLAlchemy Comment Repository Implementation"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.comment import Comment
from app.domain.repositories.comment_repository import ICommentRepository
from app.db import models


class SQLAlchemyCommentRepository(ICommentRepository):
    """Concrete implementation of Comment Repository using SQLAlchemy"""
    
    def __init__(self, db: Session):
        self._db = db
    
    def _to_domain(self, db_comment: models.Comment) -> Comment:
        """Convert ORM model to domain entity"""
        return Comment(
            id=db_comment.id,
            ad_id=db_comment.ad_id,
            user_id=db_comment.user_id,
            content=db_comment.content,
            rating=db_comment.rating,
            created_at=db_comment.created_at,
            updated_at=db_comment.updated_at
        )
    
    def _to_orm(self, comment: Comment) -> models.Comment:
        """Convert domain entity to ORM model"""
        return models.Comment(
            id=comment.id,
            ad_id=comment.ad_id,
            user_id=comment.user_id,
            content=comment.content,
            rating=comment.rating
        )
    
    async def get_by_id(self, comment_id: int) -> Optional[Comment]:
        """Get comment by ID"""
        db_comment = self._db.query(models.Comment).filter(
            models.Comment.id == comment_id
        ).first()
        return self._to_domain(db_comment) if db_comment else None
    
    async def get_by_ad(self, ad_id: int) -> List[Comment]:
        """Get all comments for an ad"""
        db_comments = self._db.query(models.Comment).filter(
            models.Comment.ad_id == ad_id
        ).order_by(models.Comment.created_at.desc()).all()
        
        return [self._to_domain(c) for c in db_comments]
    
    async def create(self, comment: Comment) -> Comment:
        """Create new comment"""
        db_comment = self._to_orm(comment)
        self._db.add(db_comment)
        self._db.commit()
        self._db.refresh(db_comment)
        return self._to_domain(db_comment)
    
    async def update(self, comment: Comment) -> Comment:
        """Update comment"""
        db_comment = self._db.query(models.Comment).filter(
            models.Comment.id == comment.id
        ).first()
        if db_comment:
            db_comment.content = comment.content
            db_comment.rating = comment.rating
            
            self._db.commit()
            self._db.refresh(db_comment)
            return self._to_domain(db_comment)
        return comment
    
    async def delete(self, comment_id: int) -> bool:
        """Delete comment"""
        db_comment = self._db.query(models.Comment).filter(
            models.Comment.id == comment_id
        ).first()
        if db_comment:
            self._db.delete(db_comment)
            self._db.commit()
            return True
        return False
