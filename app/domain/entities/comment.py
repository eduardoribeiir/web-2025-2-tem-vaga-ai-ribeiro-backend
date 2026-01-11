"""Comment domain entity"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Comment:
    """Pure domain entity for Comment"""
    ad_id: int
    user_id: int
    content: str
    
    id: Optional[int] = None
    rating: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate business rules"""
        if not self.content or len(self.content.strip()) == 0:
            raise ValueError("Comment content cannot be empty")
        if self.rating is not None and (self.rating < 1 or self.rating > 5):
            raise ValueError("Rating must be between 1 and 5")
    
    def is_owned_by(self, user_id: int) -> bool:
        """Check if comment belongs to user"""
        return self.user_id == user_id
