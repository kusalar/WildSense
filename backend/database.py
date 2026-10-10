import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    import models  # noqa
    Base.metadata.create_all(bind=engine)

    # Safe SQLite column migration for new Task 2 fields
    if DATABASE_URL.startswith("sqlite"):
        with engine.connect() as conn:
            try:
                res = conn.execute(text("PRAGMA table_info(sessions)")).fetchall()
                existing_cols = {row[1] for row in res}
                
                new_cols = {
                    "uncertainty": "TEXT",
                    "mission_why": "TEXT",
                    "observation_goal": "TEXT",
                    "curiosity_fact": "TEXT",
                    "next_suggestion": "TEXT"
                }
                for col_name, col_type in new_cols.items():
                    if col_name not in existing_cols:
                        conn.execute(text(f"ALTER TABLE sessions ADD COLUMN {col_name} {col_type}"))
                conn.commit()
            except Exception:
                pass

    # Seed plant database if empty
    seed_plants_if_empty()


def seed_plants_if_empty():
    """Seed the plants table with rich botanical encyclopedia profiles if empty."""
    import json
    from models import PlantRecord
    try:
        from data.plants_seed import PLANTS_SEED_DATA
    except ImportError:
        try:
            from backend.data.plants_seed import PLANTS_SEED_DATA
        except ImportError:
            return 0

    db = SessionLocal()
    try:
        count = db.query(PlantRecord).count()
        if count == 0:
            records = []
            for p in PLANTS_SEED_DATA:
                rec = PlantRecord(
                    id=p["id"],
                    scientific_name=p["scientific_name"],
                    canonical_name=p["canonical_name"],
                    family=p["family"],
                    genus=p["genus"],
                    species=p["species"],
                    synonyms=json.dumps(p.get("synonyms", []), ensure_ascii=False),
                    common_names=json.dumps(p.get("common_names", []), ensure_ascii=False),
                    regional_names=json.dumps(p.get("regional_names", {}), ensure_ascii=False),
                    category=p["category"],
                    growth_type=p.get("growth_type", "herb"),
                    habitat=p.get("habitat", ""),
                    flowering_season=p.get("flowering_season", ""),
                    description=p.get("description", ""),
                    distinguishing_characteristics=p.get("distinguishing_characteristics", ""),
                    safety_notes=p.get("safety_notes", ""),
                    confusable_species=json.dumps(p.get("confusable_species", []), ensure_ascii=False),
                    image_url=p.get("image_url", None),
                )
                records.append(rec)
            db.bulk_save_objects(records)
            db.commit()
            return len(records)
        return count
    except Exception as e:
        db.rollback()
        print(f"Plant seeding error: {e}")
        return 0
    finally:
        db.close()

