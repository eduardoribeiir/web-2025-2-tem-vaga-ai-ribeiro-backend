from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import json

class AdStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RESERVED = "reserved"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AdBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Título do anúncio")
    description: str = Field(..., min_length=10, description="Descrição do anúncio")
    seller: Optional[str] = Field(None, min_length=2, max_length=100, description="Nome do vendedor/anunciante")
    location: Optional[str] = Field(None, min_length=2, max_length=200, description="Localização")
    cep: Optional[str] = Field(None, max_length=10, description="CEP")
    price: Optional[float] = Field(None, ge=0, description="Preço")
    category_id: int = Field(..., description="ID da categoria")
    bedrooms: Optional[int] = Field(None, ge=0, le=20, description="Número de quartos")
    bathrooms: Optional[int] = Field(None, ge=0, le=20, description="Número de banheiros")
    rules: Optional[List[str]] = Field(None, description="Regras selecionadas")
    amenities: Optional[List[str]] = Field(None, description="Comodidades selecionadas")
    custom_rules: Optional[str] = Field(None, max_length=500, description="Regras customizadas")
    custom_amenities: Optional[str] = Field(None, max_length=500, description="Comodidades customizadas")
    images: Optional[List[str]] = Field(None, description="URLs das imagens")
    status: AdStatus = Field(default=AdStatus.PUBLISHED, description="Status do anúncio")

class AdCreate(AdBase):
    pass

class AdUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    seller: Optional[str] = Field(None, min_length=2, max_length=100)
    location: Optional[str] = Field(None, min_length=2, max_length=200)
    cep: Optional[str] = Field(None, max_length=10)
    price: Optional[float] = Field(None, ge=0)
    category_id: Optional[int] = None
    bedrooms: Optional[int] = Field(None, ge=0, le=20)
    bathrooms: Optional[int] = Field(None, ge=0, le=20)
    rules: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    custom_rules: Optional[str] = Field(None, max_length=500)
    custom_amenities: Optional[str] = Field(None, max_length=500)
    images: Optional[List[str]] = None
    status: Optional[AdStatus] = None

class AdRead(AdBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None  # Data da última publicação/republicação
    
    @field_validator('rules', 'amenities', 'images', mode='before')
    @classmethod
    def parse_json_field(cls, v):
        """Converte string JSON em lista"""
        if v is None:
            return []
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                return parsed if isinstance(parsed, list) else []
            except (json.JSONDecodeError, TypeError):
                return []
        if isinstance(v, list):
            return v
        return []
    
    class Config:
        from_attributes = True

class AdReadWithOwner(AdRead):
    owner: 'UserRead'
    category: 'CategoryRead'
    
class AdReadWithDetails(AdReadWithOwner):
    is_favorited: bool = False
    comments_count: int = 0

# Import necessário para evitar circular import
from app.schemas.user import UserRead
from app.schemas.category import CategoryRead

AdReadWithOwner.model_rebuild()
AdReadWithDetails.model_rebuild()
