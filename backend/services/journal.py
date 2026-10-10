from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from models import SessionRecord
from services.grass_score import calculate_grass_score

class JournalService:
    @staticmethod
    def create_session(
        db: Session,
        object_name: str,
        category: str,
        confidence: float,
        description: Optional[str] = None,
        uncertainty: Optional[str] = None,
        image_url: Optional[str] = None
    ) -> SessionRecord:
        record = SessionRecord(
            object_name=object_name,
            category=category,
            confidence=confidence,
            description=description,
            uncertainty=uncertainty,
            image_url=image_url,
            status="started"
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def update_mission(
        db: Session,
        session_id: str,
        mission_title: str,
        mission_instruction: str,
        estimated_minutes: int,
        physical_action: str,
        safety_note: str,
        mission_why: Optional[str] = None,
        observation_goal: Optional[str] = None
    ) -> Optional[SessionRecord]:
        record = db.query(SessionRecord).filter(SessionRecord.id == session_id).first()
        if not record:
            return None
        record.mission_title = mission_title
        record.mission_instruction = mission_instruction
        record.mission_why = mission_why
        record.mission_time_estimate = estimated_minutes
        record.physical_action = physical_action
        record.observation_goal = observation_goal
        record.safety_note = safety_note
        record.status = "field_active"
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def complete_session(
        db: Session,
        session_id: str,
        screen_time_seconds: int,
        field_time_seconds: int,
        user_observation: Optional[str],
        ai_reflection: Optional[str],
        curiosity_fact: Optional[str] = None,
        next_suggestion: Optional[str] = None
    ) -> Optional[SessionRecord]:
        record = db.query(SessionRecord).filter(SessionRecord.id == session_id).first()
        if not record:
            return None

        metrics = calculate_grass_score(
            screen_time_seconds=screen_time_seconds,
            field_time_seconds=field_time_seconds,
            user_observation=user_observation,
            is_completed=True
        )

        record.completed_at = datetime.now(timezone.utc)
        record.screen_time_seconds = screen_time_seconds
        record.field_time_seconds = field_time_seconds
        record.grass_score = metrics["grass_score"]
        record.ratio = metrics["ratio"]
        record.user_observation = user_observation
        record.ai_reflection = ai_reflection
        record.curiosity_fact = curiosity_fact
        record.next_suggestion = next_suggestion
        record.status = "completed"

        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def list_journal_entries(db: Session, limit: int = 50) -> List[SessionRecord]:
        return (
            db.query(SessionRecord)
            .filter(SessionRecord.status == "completed")
            .order_by(SessionRecord.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_stats(db: Session) -> Dict[str, Any]:
        completed = db.query(SessionRecord).filter(SessionRecord.status == "completed").all()
        if not completed:
            return {
                "total_sessions": 0,
                "total_field_time_seconds": 0,
                "total_screen_time_seconds": 0,
                "average_grass_score": 0,
                "average_ratio": 0.0,
                "species_observed": 0
            }

        total_field = sum(s.field_time_seconds for s in completed)
        total_screen = sum(s.screen_time_seconds for s in completed)
        avg_score = int(sum(s.grass_score for s in completed) / len(completed))
        avg_ratio = round(sum(s.ratio for s in completed) / len(completed), 1)
        unique_species = len(set(s.object_name for s in completed))

        return {
            "total_sessions": len(completed),
            "total_field_time_seconds": total_field,
            "total_screen_time_seconds": total_screen,
            "average_grass_score": avg_score,
            "average_ratio": avg_ratio,
            "species_observed": unique_species
        }
