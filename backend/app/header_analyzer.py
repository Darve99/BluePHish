import re
from typing import Any


class HeaderAnalyzer:
    def analyze(self, headers: dict[str, Any]) -> dict[str, Any]:
        received = headers.get("received", [])
        if isinstance(received, str):
            received = [received]

        received_entries = [entry.strip() for entry in received if isinstance(entry, str) and entry.strip()]
        origin_hosts = []
        for entry in received_entries:
            host_match = re.search(r"by\s+([\w.-]+)", entry, re.IGNORECASE)
            if host_match:
                origin_hosts.append(host_match.group(1))

        return {
            "received_count": len(received_entries),
            "origin_hosts": origin_hosts,
            "return_path": headers.get("return-path", ""),
            "reply_to": headers.get("reply-to", ""),
            "has_multiple_received": len(received_entries) > 1,
        }


header_analyzer = HeaderAnalyzer()
