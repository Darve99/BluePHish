from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AnalysisEntryDB(Base):
    __tablename__ = "analysis_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    subject = Column(String, nullable=True)
    score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    indicators = Column(Text, nullable=True)  # JSON serialized list


class RuleDB(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    weight = Column(Integer, default=1, nullable=False)
    description = Column(Text, nullable=True)
