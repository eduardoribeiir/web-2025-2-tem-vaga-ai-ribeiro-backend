"""User Service - Authentication and user management business logic"""
from typing import Optional
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.core import security
from app.core.exceptions import (
    NotFoundException,
    ConflictException,
    UnauthorizedException
)


class UserService:
    """Service layer for User business logic"""
    
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository
    
    async def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return await self._user_repository.get_by_email(email)
    
    async def register_user(self, email: str, name: str, password: str) -> tuple[User, str]:
        """Register new user and return user + JWT token"""
        # Check if email exists
        if await self._user_repository.email_exists(email):
            raise ConflictException("Email already registered")
        
        # Hash password
        hashed_password = security.get_password_hash(password)
        
        # Create user domain entity
        user = User(
            email=email,
            name=name,
            hashed_password=hashed_password
        )
        
        # Persist user
        created_user = await self._user_repository.create(user)
        
        # Generate token
        access_token = security.create_access_token(
            data={"user_id": created_user.id, "email": created_user.email}
        )
        
        return created_user, access_token
    
    async def authenticate_user(self, email: str, password: str) -> tuple[User, str]:
        """Authenticate user and return user + JWT token"""
        # Get user
        user = await self.get_user_by_email(email)
        
        # Verify user exists and password is correct
        if not user or not security.verify_password(password, user.hashed_password):
            raise UnauthorizedException("Invalid credentials")
        
        # Generate token
        access_token = security.create_access_token(
            data={"user_id": user.id, "email": user.email}
        )
        
        return user, access_token
    
    async def update_user(self, user_id: int, updates: dict) -> User:
        """Update user information"""
        user = await self.get_user_by_id(user_id)
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(user, key) and value is not None and key != 'hashed_password':
                setattr(user, key, value)
        
        return await self._user_repository.update(user)
    
    async def change_password(self, user_id: int, new_password: str) -> User:
        """Change user password"""
        user = await self.get_user_by_id(user_id)
        user.hashed_password = security.get_password_hash(new_password)
        return await self._user_repository.update(user)
