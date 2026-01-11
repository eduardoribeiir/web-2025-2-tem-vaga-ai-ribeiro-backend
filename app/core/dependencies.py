"""Dependency Injection Container - Manages service instantiation"""
from functools import lru_cache
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.domain.repositories.ad_repository import IAdRepository
from app.domain.repositories.user_repository import IUserRepository
from app.domain.repositories.comment_repository import ICommentRepository
from app.infrastructure.repositories.ad_repository import SQLAlchemyAdRepository
from app.infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from app.infrastructure.repositories.comment_repository import SQLAlchemyCommentRepository
from app.application.services.ad_service import AdService
from app.application.services.user_service import UserService
from app.application.services.comment_service import CommentService


class ServiceContainer:
    """
    Dependency Injection Container following Dependency Inversion Principle
    Services depend on interfaces, not concrete implementations
    """
    
    def __init__(self, db: Session):
        self._db = db
        self._repositories = {}
        self._services = {}
    
    def get_ad_repository(self) -> IAdRepository:
        """Get Ad Repository instance"""
        if 'ad_repository' not in self._repositories:
            self._repositories['ad_repository'] = SQLAlchemyAdRepository(self._db)
        return self._repositories['ad_repository']
    
    def get_user_repository(self) -> IUserRepository:
        """Get User Repository instance"""
        if 'user_repository' not in self._repositories:
            self._repositories['user_repository'] = SQLAlchemyUserRepository(self._db)
        return self._repositories['user_repository']
    
    def get_comment_repository(self) -> ICommentRepository:
        """Get Comment Repository instance"""
        if 'comment_repository' not in self._repositories:
            self._repositories['comment_repository'] = SQLAlchemyCommentRepository(self._db)
        return self._repositories['comment_repository']
    
    def get_ad_service(self) -> AdService:
        """Get Ad Service instance"""
        if 'ad_service' not in self._services:
            self._services['ad_service'] = AdService(
                ad_repository=self.get_ad_repository()
            )
        return self._services['ad_service']
    
    def get_user_service(self) -> UserService:
        """Get User Service instance"""
        if 'user_service' not in self._services:
            self._services['user_service'] = UserService(
                user_repository=self.get_user_repository()
            )
        return self._services['user_service']
    
    def get_comment_service(self) -> CommentService:
        """Get Comment Service instance"""
        if 'comment_service' not in self._services:
            self._services['comment_service'] = CommentService(
                comment_repository=self.get_comment_repository(),
                ad_repository=self.get_ad_repository()
            )
        return self._services['comment_service']


def get_service_container(db: Session = None) -> ServiceContainer:
    """Factory function to get service container"""
    if db is None:
        db = next(get_db())
    return ServiceContainer(db)
