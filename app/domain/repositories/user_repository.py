"""User Repository Interface"""
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User


class IUserRepository(ABC):
    """Repository interface for User entity"""
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create new user"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update user"""
        pass
    
    @abstractmethod
    async def email_exists(self, email: str) -> bool:
        """Check if email is already registered"""
        pass
