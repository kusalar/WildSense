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
