from typing import Any

from app.db_persistence import db_persistence


class HistoryService:
    def __init__(self) -> None:
        # All data operations use db_persistence
        pass

    def add_entry(self, user_email: str, analysis: dict[str, Any]) -> dict[str, Any]:
        entry = db_persistence.add_analysis_entry(
            user_email=user_email,
            subject=analysis.get("subject", ""),
            score=analysis.get("score", 0),
            risk_level=analysis.get("risk_level", "low"),
            summary=analysis.get("summary", ""),
            indicators=analysis.get("indicators", []),
        )
        return {
            "id": entry.id,
            "user_email": entry.user_email,
            "created_at": entry.created_at.isoformat() if entry.created_at else "",
            "subject": entry.subject,
            "score": entry.score,
            "risk_level": entry.risk_level,
            "summary": entry.summary,
            "indicators": analysis.get("indicators", []),
        }

    def list_for_user(self, user_email: str) -> list[dict[str, Any]]:
        entries = db_persistence.get_user_history(user_email)
        return [
            {
                "id": entry.id,
                "user_email": entry.user_email,
                "created_at": entry.created_at.isoformat() if entry.created_at else "",
                "subject": entry.subject,
                "score": entry.score,
                "risk_level": entry.risk_level,
                "summary": entry.summary,
                "indicators": entry.indicators,
            }
            for entry in entries
        ]


history_service = HistoryService()
