import re
from typing import Any
from urllib.parse import urlparse


class URLAnalyzer:
    def analyze(self, urls: list[str]) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for url in urls:
            parsed = urlparse(url)
            hostname = parsed.hostname or ""
            tld = hostname.split(".")[-1].lower() if hostname else ""
            is_https = parsed.scheme.lower() == "https"
            is_shortened = any(token in url.lower() for token in ["bit.ly", "tinyurl", "t.co", "goo.gl", "ow.ly"])
            has_ip = bool(re.match(r"^\d+\.\d+\.\d+\.\d+$", hostname or ""))
            is_suspicious = (
                not is_https
                or is_shortened
                or has_ip
                or len(hostname) > 20
                or any(token in hostname.lower() for token in ["login", "verify", "secure", "support", "account"])
            )

            results.append(
                {
                    "url": url,
                    "scheme": parsed.scheme,
                    "domain": hostname,
                    "tld": tld,
                    "is_https": is_https,
                    "is_shortened": is_shortened,
                    "has_ip": has_ip,
                    "is_suspicious": is_suspicious,
                    "risk_reason": self._risk_reason(is_https, is_shortened, has_ip, hostname),
                }
            )
        return results

    def _risk_reason(self, is_https: bool, is_shortened: bool, has_ip: bool, hostname: str) -> str:
        reasons: list[str] = []
        if not is_https:
            reasons.append("HTTP en lugar de HTTPS")
        if is_shortened:
            reasons.append("URL acortada")
        if has_ip:
            reasons.append("IP directa en el host")
        if len(hostname) > 20:
            reasons.append("Dominio largo")
        if not reasons:
            return "Sin señales claras de sospecha"
        return "; ".join(reasons)


url_analyzer = URLAnalyzer()
