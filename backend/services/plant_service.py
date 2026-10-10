"""Botanical encyclopedia and plant knowledge service for WildSense.

Provides fast multi-index searching across scientific names, common names,
synonyms, verified regional names (Hindi, Bengali, Tamil, etc.), categories,
and distinguishing characteristics.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
import json
import re

from models import PlantRecord


class PlantService:
    @staticmethod
    def get_plant_by_id(db: Session, plant_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific plant profile by its slug ID."""
        record = db.query(PlantRecord).filter(PlantRecord.id == plant_id).first()
        return record.to_dict() if record else None

    @staticmethod
    def get_plant_by_scientific_name(db: Session, name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a plant by canonical or scientific binomial name."""
        clean_name = name.strip()
        record = db.query(PlantRecord).filter(
            or_(
                func.lower(PlantRecord.canonical_name) == clean_name.lower(),
                func.lower(PlantRecord.scientific_name) == clean_name.lower()
            )
        ).first()
        if not record:
            # Try prefix / wildcard
            record = db.query(PlantRecord).filter(
                PlantRecord.canonical_name.ilike(f"{clean_name}%")
            ).first()
        return record.to_dict() if record else None

    @staticmethod
    def list_plants(
        db: Session,
        category: Optional[str] = None,
        growth_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 120
    ) -> List[Dict[str, Any]]:
        """List plants with optional category/growth_type filters."""
        query = db.query(PlantRecord)
        if category and category.lower() != "all":
            query = query.filter(PlantRecord.category == category.lower())
        if growth_type and growth_type.lower() != "all":
            query = query.filter(PlantRecord.growth_type == growth_type.lower())
        
        records = query.order_by(PlantRecord.canonical_name.asc()).offset(skip).limit(limit).all()
        return [r.to_dict() for r in records]

    @staticmethod
    def get_categories(db: Session) -> List[Dict[str, Any]]:
        """Get all available plant categories with species counts."""
        results = db.query(
            PlantRecord.category,
            func.count(PlantRecord.id).label("count")
        ).group_by(PlantRecord.category).all()
        return [{"category": row[0], "count": row[1]} for row in results]

    @staticmethod
    def search_plants(
        db: Session,
        query_str: str,
        category: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Search botanical database across:
        - Canonical and scientific binomial names
        - Common names (English / international)
        - Regional names (Devanagari Hindi, Bengali script, transliterations)
        - Botanical Family and Genus
        - Distinguishing traits and descriptions
        """
        q = query_str.strip()
        if not q:
            return PlantService.list_plants(db, category=category, limit=limit)

        q_lower = q.lower()
        search_filter = or_(
            PlantRecord.canonical_name.ilike(f"%{q}%"),
            PlantRecord.scientific_name.ilike(f"%{q}%"),
            PlantRecord.genus.ilike(f"%{q}%"),
            PlantRecord.family.ilike(f"%{q}%"),
            PlantRecord.common_names.ilike(f"%{q}%"),
            PlantRecord.regional_names.ilike(f"%{q}%"),
            PlantRecord.synonyms.ilike(f"%{q}%"),
            PlantRecord.distinguishing_characteristics.ilike(f"%{q}%"),
            PlantRecord.description.ilike(f"%{q}%"),
        )

        db_query = db.query(PlantRecord).filter(search_filter)
        if category and category.lower() != "all":
            db_query = db_query.filter(PlantRecord.category == category.lower())

        records = db_query.all()

        # Score & rank results for relevance
        def score_record(rec: PlantRecord) -> int:
            score = 0
            c_name = rec.canonical_name.lower()
            s_name = rec.scientific_name.lower()
            c_names = rec.common_names.lower()
            r_names = rec.regional_names.lower()
            fam = rec.family.lower()
            gen = rec.genus.lower()

            # Exact canonical name
            if c_name == q_lower:
                score += 100
            elif c_name.startswith(q_lower):
                score += 80
            elif q_lower in c_name:
                score += 60

            # Common names match
            if f'"{q_lower}"' in c_names or f' {q_lower} ' in c_names:
                score += 70
            elif q_lower in c_names:
                score += 50

            # Regional name match (Hindi / Bengali)
            if q_lower in r_names:
                score += 65

            # Genus / Family match
            if gen == q_lower:
                score += 50
            elif fam == q_lower:
                score += 40

            # Characteristics
            if q_lower in rec.distinguishing_characteristics.lower():
                score += 20
            if q_lower in rec.description.lower():
                score += 10

            return score

        scored = [(score_record(r), r) for r in records]
        scored.sort(key=lambda x: x[0], reverse=True)

        return [r.to_dict() for _, r in scored[:limit]]
