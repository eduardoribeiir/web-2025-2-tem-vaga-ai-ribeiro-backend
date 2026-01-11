"""Ad domain entity - Independent of database and frameworks"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class AdStatus(str, Enum):
    """Status lifecycle of an ad"""
    DRAFT = "draft"
    PUBLISHED = "published"
    RESERVED = "reserved"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Ad:
    """Pure domain entity for Ad - No ORM, No framework dependencies"""
    title: str
    description: str
    price: float
    category_id: int
    user_id: int
    
    # Optional fields
    id: Optional[int] = None
    seller: Optional[str] = None
    location: Optional[str] = None
    cep: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    rules: List[str] = field(default_factory=list)
    amenities: List[str] = field(default_factory=list)
    custom_rules: Optional[str] = None
    custom_amenities: Optional[str] = None
    images: List[str] = field(default_factory=list)
    status: AdStatus = AdStatus.PUBLISHED
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None  # Data da última publicação
    
    def __post_init__(self):
        """Validate business rules"""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if self.bedrooms is not None and self.bedrooms < 0:
            raise ValueError("Bedrooms cannot be negative")
        if self.bathrooms is not None and self.bathrooms < 0:
            raise ValueError("Bathrooms cannot be negative")
    
    def is_owned_by(self, user_id: int) -> bool:
        """Check if ad belongs to user"""
        return self.user_id == user_id
    
    def can_transition_to(self, new_status: AdStatus) -> bool:
        """Validate status transitions according to business rules"""
        valid_transitions = {
            AdStatus.DRAFT: [AdStatus.PUBLISHED, AdStatus.CANCELLED],
            AdStatus.PUBLISHED: [AdStatus.RESERVED, AdStatus.CANCELLED],
            AdStatus.RESERVED: [AdStatus.COMPLETED, AdStatus.PUBLISHED],
            AdStatus.COMPLETED: [],
            AdStatus.CANCELLED: [AdStatus.DRAFT, AdStatus.PUBLISHED]
        }
        return new_status in valid_transitions.get(self.status, [])
    
    def change_status(self, new_status: AdStatus) -> None:
        """Change status with validation"""
        if not self.can_transition_to(new_status):
            raise ValueError(
                f"Invalid status transition from {self.status} to {new_status}"
            )
        self.status = new_status
