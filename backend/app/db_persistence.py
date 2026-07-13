import json
from typing import Any

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import AnalysisEntryDB, RuleDB, UserDB


class DatabasePersistence:
    """SQLAlchemy-based persistence layer for BluePHish"""

    def get_user_by_email(self, email: str) -> UserDB | None:
        db = SessionLocal()
        try:
            return db.query(UserDB).filter(UserDB.email == email).first()
        finally:
            db.close()

    def get_user_by_id(self, user_id: int) -> UserDB | None:
        db = SessionLocal()
        try:
            return db.query(UserDB).filter(UserDB.id == user_id).first()
        finally:
            db.close()

    def create_user(self, name: str, email: str, password_hash: str, role: str = "user") -> UserDB:
        db = SessionLocal()
        try:
            user = UserDB(name=name, email=email, password_hash=password_hash, role=role)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        finally:
            db.close()

    def get_all_users(self) -> list[UserDB]:
        db = SessionLocal()
        try:
            return db.query(UserDB).all()
        finally:
            db.close()

    def add_analysis_entry(
        self,
        user_email: str,
        subject: str,
        score: float,
        risk_level: str,
        summary: str,
        indicators: list[str],
    ) -> AnalysisEntryDB:
        db = SessionLocal()
        try:
            entry = AnalysisEntryDB(
                user_email=user_email,
                subject=subject,
                score=score,
                risk_level=risk_level,
                summary=summary,
                indicators=json.dumps(indicators),
            )
            db.add(entry)
            db.commit()
            db.refresh(entry)
            return entry
        finally:
            db.close()

    def get_user_history(self, user_email: str) -> list[AnalysisEntryDB]:
        db = SessionLocal()
        try:
            return db.query(AnalysisEntryDB).filter(AnalysisEntryDB.user_email == user_email).all()
        finally:
            db.close()

    def get_all_rules(self) -> list[RuleDB]:
        db = SessionLocal()
        try:
            return db.query(RuleDB).all()
        finally:
            db.close()

    def get_rule_by_id(self, rule_id: int) -> RuleDB | None:
        db = SessionLocal()
        try:
            return db.query(RuleDB).filter(RuleDB.id == rule_id).first()
        finally:
            db.close()

    def update_rule(self, rule_id: int, weight: int) -> RuleDB | None:
        db = SessionLocal()
        try:
            rule = db.query(RuleDB).filter(RuleDB.id == rule_id).first()
            if rule:
                rule.weight = weight
                db.commit()
                db.refresh(rule)
            return rule
        finally:
            db.close()

    def create_rule(self, name: str, weight: int, description: str = None) -> RuleDB:
        db = SessionLocal()
        try:
            rule = RuleDB(name=name, weight=weight, description=description)
            db.add(rule)
            db.commit()
            db.refresh(rule)
            return rule
        finally:
            db.close()


db_persistence = DatabasePersistence()
