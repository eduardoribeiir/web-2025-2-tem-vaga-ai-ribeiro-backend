"""User domain entity"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Pure domain entity for User"""
    email: str
    name: str
    hashed_password: str
    
    id: Optional[int] = None
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate business rules"""
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email format")
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Name cannot be empty")
