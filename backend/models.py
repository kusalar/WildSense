import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, Float, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class SessionRecord(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Identification
    object_name: Mapped[str] = mapped_column(String, nullable=False, default="Unknown Nature Object")
    category: Mapped[str] = mapped_column(String, nullable=False, default="other")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    uncertainty: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Mission
    mission_title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    mission_instruction: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mission_why: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mission_time_estimate: Mapped[int] = mapped_column(Integer, default=2)  # minutes
    physical_action: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    observation_goal: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    safety_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Engagement & Grass Metrics
    screen_time_seconds: Mapped[int] = mapped_column(Integer, default=0)
    field_time_seconds: Mapped[int] = mapped_column(Integer, default=0)
    grass_score: Mapped[int] = mapped_column(Integer, default=0)
    ratio: Mapped[float] = mapped_column(Float, default=0.0)

    # Reflection
    user_observation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_reflection: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    curiosity_fact: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    next_suggestion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Status: 'started', 'field_active', 'completed', 'abandoned'
    status: Mapped[str] = mapped_column(String, default="started")
