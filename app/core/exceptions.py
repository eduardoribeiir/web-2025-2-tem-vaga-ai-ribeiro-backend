"""Custom exceptions for better error handling"""


class DomainException(Exception):
    """Base exception for domain errors"""
    pass


class NotFoundException(DomainException):
    """Resource not found exception"""
    pass


class ForbiddenException(DomainException):
    """Forbidden action exception"""
    pass


class BusinessRuleException(DomainException):
    """Business rule validation exception"""
    pass


class UnauthorizedException(DomainException):
    """Unauthorized action exception"""
    pass


class ConflictException(DomainException):
    """Conflict exception (e.g., duplicate email)"""
    pass
