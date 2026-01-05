from sqlalchemy import Boolean, Column, Integer, String, Float, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Tabela de associação para favoritos (many-to-many)
favorites_table = Table(
    'favorites',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('ad_id', Integer, ForeignKey('ads.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

class User(Base):
    """Modelo de Usuário"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    ads = relationship("Ad", back_populates="owner", cascade="all, delete-orphan")
    favorites = relationship("Ad", secondary=favorites_table, back_populates="favorited_by")

class Category(Base):
    """Modelo de Categoria"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    ads = relationship("Ad", back_populates="category")

class Ad(Base):
    """Modelo de Anúncio"""
    __tablename__ = "ads"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    seller = Column(String, nullable=False)
    location = Column(String, nullable=False, index=True)
    cep = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    
    rules = Column(Text, nullable=True)  # JSON string
    amenities = Column(Text, nullable=True)  # JSON string
    custom_rules = Column(Text, nullable=True)
    custom_amenities = Column(Text, nullable=True)
    images = Column(Text, nullable=True)  # JSON string
    
    status = Column(String, default="published")  # draft, published
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    owner = relationship("User", back_populates="ads")
    category = relationship("Category", back_populates="ads")
    favorited_by = relationship("User", secondary=favorites_table, back_populates="favorites")
    comments = relationship("Comment", back_populates="ad", cascade="all, delete-orphan")

class Comment(Base):
    """Modelo de Comentário"""
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    ad_id = Column(Integer, ForeignKey("ads.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    content = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)  # 1-5 estrelas
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    ad = relationship("Ad", back_populates="comments")
    user = relationship("User")
