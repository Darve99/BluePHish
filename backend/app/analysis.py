import re
from typing import Any

from app.header_analyzer import header_analyzer
from app.parser import parse_email_content
from app.url_analyzer import url_analyzer


class RuleEngine:
    def __init__(self, rules: list[dict[str, Any]] | None = None) -> None:
        self.rules = rules or [
            {
                "id": "missing_sender",
                "description": "No se encontró remitente en los headers",
                "weight": 8,
                "applies": lambda ctx: not ctx["sender"],
            },
            {
                "id": "suspicious_sender",
                "description": "Remitente sospechoso o que finge ser oficial",
                "weight": 25,
                "applies": lambda ctx: bool(ctx["sender"]) and any(pattern in ctx["sender"].lower() for pattern in ["no-reply", "support", "security", "admin", "paypal", "microsoft", "google", "amazon", "banco", "seguridad"]),
            },
            {
                "id": "credential_request",
                "description": "Se solicitan credenciales (contraseña, usuario, token)",
                "weight": 35,
                "applies": lambda ctx: any(term in ctx["body"].lower() for term in ["contraseña", "password", "usuario", "username", "código", "pin", "token", "autenticación", "credential"]),
            },
            {
                "id": "urgent_language",
                "description": "Lenguaje de urgencia extrema",
                "weight": 20,
                "applies": lambda ctx: any(term in ctx["body"].lower() for term in ["24 hora", "24 horas", "inmediatamente", "inmediato", "ahora", "urgente", "suspendida", "bloqueada", "congelada", "desactivada"]),
            },
            {
                "id": "typosquatting_domain",
                "description": "Dominio con typosquatting (caracteres similares confusos)",
                "weight": 30,
                "applies": lambda ctx: any(
                    any(char in url.lower() for char in ["0l", "l0", "rn", "1l", "5s"])
                    for url in ctx["urls"]
                ),
            },
            {
                "id": "verify_identity",
                "description": "Se pide verificar identidad o reactivar cuenta",
                "weight": 25,
                "applies": lambda ctx: any(term in ctx["body"].lower() for term in ["verificar", "verify", "reactivar", "reactivate", "confirmar identidad", "validate", "confirm identity"]),
            },
            {
                "id": "many_urls",
                "description": "Se detectaron múltiples enlaces",
                "weight": 10,
                "applies": lambda ctx: len(ctx["urls"]) > 3,
            },
            {
                "id": "insecure_url",
                "description": "Se encontró un enlace HTTP sin encripción",
                "weight": 15,
                "applies": lambda ctx: any(url.lower().split("://", 1)[0] == "http" for url in ctx["urls"]),
            },
            {
                "id": "shortened_url",
                "description": "Se detectaron acortadores de URL",
                "weight": 20,
                "applies": lambda ctx: any("bit.ly" in url or "tinyurl" in url or "t.co" in url for url in ctx["urls"]),
            },
            {
                "id": "suspicious_attachment",
                "description": "Se detectó referencia a adjunto o ejecutable",
                "weight": 20,
                "applies": lambda ctx: "attachment" in ctx["body"].lower() or "exe" in ctx["body"].lower() or ".zip" in ctx["body"].lower(),
            },
            {
                "id": "spf_fail",
                "description": "El correo no presenta evidencia de SPF válida",
                "weight": 20,
                "applies": lambda ctx: ctx.get("spf") == "fail",
            },
            {
                "id": "dkim_fail",
                "description": "El correo no presenta evidencia de DKIM válida",
                "weight": 20,
                "applies": lambda ctx: ctx.get("dkim") == "fail",
            },
            {
                "id": "dmarc_fail",
                "description": "El correo no presenta evidencia de DMARC válida",
                "weight": 20,
                "applies": lambda ctx: ctx.get("dmarc") == "fail",
            },
        ]

    def evaluate(self, context: dict[str, Any]) -> tuple[int, list[dict[str, Any]]]:
        score = 0
        rule_hits: list[dict[str, Any]] = []
        for rule in self.rules:
            if rule["applies"](context):
                score += rule["weight"]
                rule_hits.append({
                    "id": rule["id"],
                    "description": rule["description"],
                    "weight": rule["weight"],
                })
        return min(score, 100), rule_hits


class EmailAnalyzer:
    def __init__(self) -> None:
        self.rule_engine = RuleEngine()

    def analyze(self, raw_email: str | bytes) -> dict[str, Any]:
        parsed = parse_email_content(raw_email)
        text = raw_email.decode("utf-8", errors="ignore") if isinstance(raw_email, bytes) else (raw_email or "")
        headers, body = self._split_headers_and_body(text)
        subject = parsed.get("subject") or self._extract_header(headers, "subject")
        sender = parsed.get("from") or self._extract_header(headers, "from")
        recipient = parsed.get("to") or self._extract_header(headers, "to")
        urls = parsed.get("urls") or self._extract_urls(text)
        suspicious_terms = [
            term for term in ["urgent", "password", "verify", "invoice", "gift card", "bank", "microsoft", "google", "amazon"]
            if term.lower() in text.lower()
        ]
        auth_results = self._analyze_auth_headers(parsed.get("headers", {}))
        url_analysis = url_analyzer.analyze(urls)
        header_analysis = header_analyzer.analyze(parsed.get("headers", {}))

        context = {
            "sender": sender,
            "body": body or parsed.get("body", ""),
            "urls": urls,
            "terms": suspicious_terms,
            **auth_results,
        }
        score, rule_hits = self.rule_engine.evaluate(context)
        risk_level = self._risk_level(score)

        return {
            "subject": subject,
            "from": sender,
            "to": recipient,
            "date": parsed.get("date", ""),
            "reply_to": parsed.get("reply_to", ""),
            "return_path": parsed.get("return_path", ""),
            "urls": urls,
            "body_preview": (body or parsed.get("body", ""))[:600],
            "headers": parsed.get("headers", {}),
            "attachments": parsed.get("attachments", []),
            "auth_results": auth_results,
            "header_analysis": header_analysis,
            "url_analysis": url_analysis,
            "indicators": [
                {"type": rule["id"], "severity": "high" if rule["weight"] >= 15 else "medium", "detail": rule["description"]}
                for rule in rule_hits
            ],
            "score": score,
            "risk_level": risk_level,
            "summary": self._build_summary(score, rule_hits, suspicious_terms),
            "suspicious_terms": suspicious_terms,
            "rule_hits": rule_hits,
        }

    def _split_headers_and_body(self, text: str) -> tuple[str, str]:
        parts = text.split("\n\n", 1)
        if len(parts) == 2 and ":" in parts[0]:
            return parts[0], parts[1]
        return "", text

    def _extract_header(self, headers: str, header_name: str) -> str:
        pattern = re.compile(rf"^{header_name}:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
        match = pattern.search(headers)
        return match.group(1).strip() if match else ""

    def _extract_urls(self, text: str) -> list[str]:
        return re.findall(r"https?://[^\s]+", text)

    def _analyze_auth_headers(self, headers: dict[str, Any]) -> dict[str, str]:
        spf = "neutral"
        dkim = "neutral"
        dmarc = "neutral"

        auth_headers = {key.lower(): value for key, value in headers.items() if isinstance(value, str)}
        if "authentication-results" in auth_headers:
            content = auth_headers["authentication-results"].lower()
            if "spf=pass" in content:
                spf = "pass"
            elif "spf=fail" in content:
                spf = "fail"
            if "dkim=pass" in content:
                dkim = "pass"
            elif "dkim=fail" in content:
                dkim = "fail"
            if "dmarc=pass" in content:
                dmarc = "pass"
            elif "dmarc=fail" in content:
                dmarc = "fail"
        return {"spf": spf, "dkim": dkim, "dmarc": dmarc}

    def _risk_level(self, score: int) -> str:
        if score >= 70:
            return "high"
        if score >= 40:
            return "medium"
        return "low"

    def _build_summary(self, score: int, rule_hits: list[dict[str, Any]], suspicious_terms: list[str]) -> str:
        base = f"Puntuación de riesgo: {score}/100."
        if rule_hits:
            base += f" Indicadores: {', '.join(item['description'] for item in rule_hits[:3])}."
        if suspicious_terms:
            base += f" Términos sospechosos detectados: {', '.join(suspicious_terms)}."
        return base


analyzer = EmailAnalyzer()
