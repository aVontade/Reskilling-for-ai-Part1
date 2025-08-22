"""
User model for authentication and user management
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime
from typing import Optional, List
import uuid

class User(Base):
    """User model for authentication and profile management"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth users
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    title = Column(String(200), nullable=True)
    department = Column(String(200), nullable=True)
    company = Column(String(200), nullable=True)
    
    # Authentication fields
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login = Column(DateTime, nullable=True)
    
    # Profile information
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    location = Column(String(200), nullable=True)
    timezone = Column(String(100), nullable=True)
    
    # Skills and preferences
    current_skills = Column(JSON, default=list)  # List of skill names
    target_skills = Column(JSON, default=list)   # Skills user wants to develop
    learning_preferences = Column(JSON, default=dict)  # Learning style preferences
    
    # Relationships
    assessments = relationship("Assessment", back_populates="user")
    learning_paths = relationship("LearningPath", back_populates="user")
    organizations = relationship("OrganizationMember", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.is_active and self.is_verified

class OrganizationMember(Base):
    """Organization membership model"""
    
    __tablename__ = "organization_members"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    role = Column(String(50), default="member")  # member, admin, owner
    joined_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="organizations")
    organization = relationship("Organization", back_populates="members")
    
    def __repr__(self):
        return f"<OrganizationMember user_id={self.user_id} org_id={self.organization_id}>"

# Import here to avoid circular imports
from sqlalchemy import ForeignKey
