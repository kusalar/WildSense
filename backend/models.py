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


class PlantRecord(Base):
    __tablename__ = "plants"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    scientific_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    canonical_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    family: Mapped[str] = mapped_column(String, nullable=False, index=True)
    genus: Mapped[str] = mapped_column(String, nullable=False, index=True)
    species: Mapped[str] = mapped_column(String, nullable=False)
    synonyms: Mapped[str] = mapped_column(Text, default="[]")
    common_names: Mapped[str] = mapped_column(Text, default="[]")
    regional_names: Mapped[str] = mapped_column(Text, default="{}")
    category: Mapped[str] = mapped_column(String, nullable=False, index=True)
    growth_type: Mapped[str] = mapped_column(String, default="herb")
    habitat: Mapped[str] = mapped_column(Text, default="")
    flowering_season: Mapped[str] = mapped_column(String, default="")
    description: Mapped[str] = mapped_column(Text, default="")
    distinguishing_characteristics: Mapped[str] = mapped_column(Text, default="")
    safety_notes: Mapped[str] = mapped_column(Text, default="")
    confusable_species: Mapped[str] = mapped_column(Text, default="[]")
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def to_dict(self):
        import json
        return {
            "id": self.id,
            "scientific_name": self.scientific_name,
            "canonical_name": self.canonical_name,
            "family": self.family,
            "genus": self.genus,
            "species": self.species,
            "synonyms": json.loads(self.synonyms) if self.synonyms else [],
            "common_names": json.loads(self.common_names) if self.common_names else [],
            "regional_names": json.loads(self.regional_names) if self.regional_names else {},
            "category": self.category,
            "growth_type": self.growth_type,
            "habitat": self.habitat,
            "flowering_season": self.flowering_season,
            "description": self.description,
            "distinguishing_characteristics": self.distinguishing_characteristics,
            "safety_notes": self.safety_notes,
            "confusable_species": json.loads(self.confusable_species) if self.confusable_species else [],
            "image_url": self.image_url,
        }

