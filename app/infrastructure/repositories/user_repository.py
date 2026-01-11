"""SQLAlchemy User Repository Implementation"""
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.db import models


class SQLAlchemyUserRepository(IUserRepository):
    """Concrete implementation of User Repository using SQLAlchemy"""
    
    def __init__(self, db: Session):
        self._db = db
    
    def _to_domain(self, db_user: models.User) -> User:
        """Convert ORM model to domain entity"""
        return User(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            hashed_password=db_user.hashed_password,
            phone=db_user.phone,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
    
    def _to_orm(self, user: User) -> models.User:
        """Convert domain entity to ORM model"""
        return models.User(
            id=user.id,
            email=user.email,
            name=user.name,
            hashed_password=user.hashed_password,
            phone=user.phone
        )
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        db_user = self._db.query(models.User).filter(models.User.id == user_id).first()
        return self._to_domain(db_user) if db_user else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        db_user = self._db.query(models.User).filter(models.User.email == email).first()
        return self._to_domain(db_user) if db_user else None
    
    async def create(self, user: User) -> User:
        """Create new user"""
        db_user = self._to_orm(user)
        self._db.add(db_user)
        self._db.commit()
        self._db.refresh(db_user)
        return self._to_domain(db_user)
    
    async def update(self, user: User) -> User:
        """Update user"""
        db_user = self._db.query(models.User).filter(models.User.id == user.id).first()
        if db_user:
            db_user.email = user.email
            db_user.name = user.name
            db_user.hashed_password = user.hashed_password
            db_user.phone = user.phone
            
            self._db.commit()
            self._db.refresh(db_user)
            return self._to_domain(db_user)
        return user
    
    async def email_exists(self, email: str) -> bool:
        """Check if email is already registered"""
        return self._db.query(models.User).filter(models.User.email == email).first() is not None
