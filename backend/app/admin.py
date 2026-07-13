from typing import Any

from app.db_persistence import db_persistence


class AdminService:
    def __init__(self) -> None:
        # All data operations use db_persistence
        pass

    def list_rules(self) -> list[dict[str, Any]]:
        rules = db_persistence.get_all_rules()
        return [
            {
                "id": rule.id,
                "name": rule.name,
                "weight": rule.weight,
                "description": rule.description,
            }
            for rule in rules
        ]

    def update_rule(self, rule_id: int, weight: int) -> dict[str, Any]:
        rule = db_persistence.update_rule(rule_id, weight)
        if not rule:
            raise ValueError("Rule not found")
        return {
            "id": rule.id,
            "name": rule.name,
            "weight": rule.weight,
            "description": rule.description,
        }

    def list_users(self) -> list[dict[str, Any]]:
        users = db_persistence.get_all_users()
        return [
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
            }
            for user in users
        ]

    def stats(self) -> dict[str, Any]:
        users = db_persistence.get_all_users()
        rules = db_persistence.get_all_rules()
        return {
            "total_users": len(users),
            "total_rules": len(rules),
            "last_analysis_score": 78,
        }


admin_service = AdminService()

