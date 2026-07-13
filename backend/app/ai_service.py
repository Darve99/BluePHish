import os
from typing import Any

import httpx


class AIService:
    def __init__(self, base_url: str | None = None, api_key: str | None = None) -> None:
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def generate_analysis_summary(self, analysis: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            return {
                "classification": "manual_review",
                "risk_level": analysis.get("risk_level", "low"),
                "explanation": "La IA no está configurada. Se usa el análisis de reglas locales.",
                "evidences": analysis.get("indicators", []),
                "recommendations": [
                    "Verifica la URL antes de hacer clic.",
                    "No proporciones credenciales ni datos sensibles.",
                ],
                "executive_summary": analysis.get("summary", "Análisis local completado."),
            }

        payload = {
            "model": "gpt-4o-mini",
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un analista de ciberseguridad especializado en phishing. Devuelve solo JSON válido con: classification, risk_level, explanation, evidences, recommendations, executive_summary.",
                },
                {
                    "role": "user",
                    "content": f"Analiza este resumen estructurado de phishing sin usar el correo completo: {analysis}",
                },
            ],
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = httpx.post(f"{self.base_url}/chat/completions", json=payload, headers=headers, timeout=20.0)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return self._parse_json(content)

    def _parse_json(self, content: str) -> dict[str, Any]:
        try:
            return __import__("json").loads(content)
        except Exception:
            return {
                "classification": "manual_review",
                "risk_level": "medium",
                "explanation": content,
                "evidences": [],
                "recommendations": ["Revisa el resultado con criterio humano."],
                "executive_summary": content,
            }


ai_service = AIService()
