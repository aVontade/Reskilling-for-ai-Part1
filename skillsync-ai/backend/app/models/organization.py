"""
Organization model for company/team management
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime
from typing import Optional, List
import uuid

class Organization(Base):
    """Organization/Company model"""
    
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    website = Column(String(500), nullable=True)
    industry = Column(String(200), nullable=True)
    size = Column(String(50), nullable=True)  # small, medium, large, enterprise
    location = Column(String(200), nullable=True)
    
    # Organization settings
    is_active = Column(Boolean, default=True)
    ai_maturity_level = Column(String(50), default="beginner")  # beginner, intermediate, advanced
    subscription_tier = Column(String(50), default="free")  # free, basic, professional, enterprise
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    members = relationship("OrganizationMember", back_populates="organization")
    assessments = relationship("OrganizationAssessment", back_populates="organization")
    learning_paths = relationship("OrganizationLearningPath", back_populates="organization")
    
    def __repr__(self):
        return f"<Organization {self.name}>"
    
    @property
    def member_count(self) -> int:
        """Get number of active members"""
        return len([m for m in self.members if m.is_active])
    
    @property
    def admin_count(self) -> int:
        """Get number of admin members"""
        return len([m for m in self.members if m.is_active and m.role in ['admin', 'owner']])

class OrganizationAssessment(Base):
    """Organization-wide assessment results"""
    
    __tablename__ = "organization_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    assessment_type = Column(String(100), nullable=False)  # ai_maturity, skills_gap, etc.
    assessment_data = Column(JSON, nullable=False)
    overall_score = Column(Integer, nullable=True)
    completed_at = Column(DateTime, default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="assessments")
    
    def __repr__(self):
        return f"<OrganizationAssessment org_id={self.organization_id} type={self.assessment_type}>"

class OrganizationLearningPath(Base):
    """Organization-wide learning path templates"""
    
    __tablename__ = "organization_learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    target_roles = Column(JSON, default=list)  # Roles this path is designed for
    required_skills = Column(JSON, default=list)  # Skills to be developed
    learning_resources = Column(JSON, default=list)  # Curated resources
    estimated_duration = Column(Integer, nullable=True)  # Hours
    difficulty_level = Column(String(50), default="beginner")  # beginner, intermediate, advanced
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="learning_paths")
    
    def __repr__(self):
        return f"<OrganizationLearningPath {self.name}>"
