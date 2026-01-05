from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000, description="Conteúdo do comentário")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Avaliação (1-5 estrelas)")

class CommentCreate(CommentBase):
    ad_id: int = Field(..., description="ID do anúncio")

class CommentUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    rating: Optional[int] = Field(None, ge=1, le=5)

class CommentRead(CommentBase):
    id: int
    ad_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CommentReadWithUser(CommentRead):
    user: 'UserRead'

from app.schemas.user import UserRead
CommentReadWithUser.model_rebuild()
