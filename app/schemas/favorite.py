from pydantic import BaseModel
from datetime import datetime

class FavoriteCreate(BaseModel):
    ad_id: int

class FavoriteRead(BaseModel):
    user_id: int
    ad_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class FavoriteToggleResponse(BaseModel):
    favorited: bool
    message: str
