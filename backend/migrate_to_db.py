"""
Migration script to move data from JSON file-based persistence to SQLAlchemy ORM.
Run this script before switching to the new persistence layer.
"""
import json
import os
from pathlib import Path

from app.database import Base, engine
from app.db_persistence import db_persistence
from app.models import AnalysisEntryDB, RuleDB, UserDB
from app.persistence import persistence


def migrate_data():
    """Migrate all data from JSON files to database."""
    print("🔄 Starting migration from JSON to SQLAlchemy ORM...")

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

    # Migrate users
    print("\n📦 Migrating users...")
    users_data = persistence.load_json("users.json", {})
    for email, user_info in users_data.items():
        existing = db_persistence.get_user_by_email(email)
        if not existing:
            db_persistence.create_user(
                name=user_info["name"],
                email=user_info["email"],
                password_hash=user_info["password_hash"],
                role=user_info.get("role", "user"),
            )
    print(f"✅ Migrated {len(users_data)} users")

    # Migrate analysis history
    print("\n📦 Migrating analysis history...")
    history_data = persistence.load_json("history.json", [])
    for entry in history_data:
        db_persistence.add_analysis_entry(
            user_email=entry["user_email"],
            subject=entry.get("subject", ""),
            score=entry.get("score", 0),
            risk_level=entry.get("risk_level", "low"),
            summary=entry.get("summary", ""),
            indicators=entry.get("indicators", []),
        )
    print(f"✅ Migrated {len(history_data)} analysis entries")

    # Create default rules
    print("\n📦 Creating default rules...")
    default_rules = [
        ("Urgent Language", 15, "Emails with urgent language patterns"),
        ("Suspicious Sender", 20, "Sender domain doesn't match organization"),
        ("Shortened URL", 18, "Presence of URL shortening services"),
    ]
    for name, weight, description in default_rules:
        try:
            db_persistence.create_rule(name=name, weight=weight, description=description)
        except Exception:
            # Rule already exists
            pass
    print(f"✅ Created {len(default_rules)} default rules")

    print("\n🎉 Migration completed successfully!")


if __name__ == "__main__":
    migrate_data()
