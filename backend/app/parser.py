import email
import re
from typing import Any


def _decode_payload(payload: Any) -> str:
    if isinstance(payload, bytes):
        return payload.decode("utf-8", errors="ignore")
    return str(payload or "")


def _collect_body_parts(message: Any) -> list[str]:
    body_parts: list[str] = []
    if not message.is_multipart():
        body_parts.append(_decode_payload(message.get_payload(decode=True)))
        return body_parts

    for part in message.walk():
        if part.get_content_type() == "text/plain" and part.get_payload(decode=True):
            body_parts.append(_decode_payload(part.get_payload(decode=True)))
        elif part.get_content_type() == "text/html" and part.get_payload(decode=True):
            text = _decode_payload(part.get_payload(decode=True))
            body_parts.append(re.sub(r"<[^>]+>", " ", text))
    return body_parts


def parse_email_content(raw_email: str | bytes) -> dict[str, Any]:
    raw_text = raw_email.decode("utf-8", errors="ignore") if isinstance(raw_email, bytes) else (raw_email or "")
    message = email.message_from_string(raw_text)
    headers = {
        "subject": message.get("subject", ""),
        "from": message.get("from", ""),
        "to": message.get("to", ""),
        "date": message.get("date", ""),
        "reply_to": message.get("reply-to", ""),
        "return_path": message.get("return-path", ""),
    }

    body = "\n".join(part for part in _collect_body_parts(message) if part).strip()
    urls = re.findall(r"https?://[^\s]+", raw_text + "\n" + body)

    return {
        "subject": headers["subject"],
        "from": headers["from"],
        "to": headers["to"],
        "date": headers["date"],
        "reply_to": headers["reply_to"],
        "return_path": headers["return_path"],
        "body": body,
        "headers": headers,
        "urls": urls,
        "attachments": [],
    }
