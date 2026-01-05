from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Nome da categoria")
    slug: str = Field(..., min_length=2, max_length=50, description="Slug da categoria")
    description: Optional[str] = Field(None, max_length=200, description="Descrição")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    slug: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=200)

class CategoryRead(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
