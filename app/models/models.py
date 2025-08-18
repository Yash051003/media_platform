from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to MediaAsset, indicating this user can have many assets
    media_assets = relationship("MediaAsset", back_populates="owner")

class MediaAsset(Base):
    __tablename__ = "media_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    file_url = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # --- THIS IS THE KEY CHANGE ---
    # Foreign key to link to the admin_users table
    owner_id = Column(Integer, ForeignKey("admin_users.id"), nullable=False)
    
    # Relationship to AdminUser, linking this asset back to its owner
    owner = relationship("AdminUser", back_populates="media_assets")

class MediaViewLog(Base):
    __tablename__ = "media_view_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    media_id = Column(Integer, ForeignKey("media_assets.id"), nullable=False)
    viewed_by_ip = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
