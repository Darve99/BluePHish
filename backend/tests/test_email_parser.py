from app.parser import parse_email_content


def test_parse_email_headers_and_urls():
    sample = """Subject: Urgent payment needed
From: support@paypal-security.com
To: victim@example.com
Date: Mon, 01 Jul 2024 10:00:00 +0000
Reply-To: help@secure-paypal.com
Return-Path: <bounce@paypal-security.com>

Hello,
Please verify your account immediately: https://bit.ly/abc123 and https://example.com
"""

    parsed = parse_email_content(sample)

    assert parsed["subject"] == "Urgent payment needed"
    assert parsed["from"] == "support@paypal-security.com"
    assert parsed["to"] == "victim@example.com"
    assert parsed["reply_to"] == "help@secure-paypal.com"
    assert parsed["return_path"] == "bounce@paypal-security.com"
    assert "https://bit.ly/abc123" in parsed["urls"]
    assert parsed["body"].startswith("Hello,")
    assert parsed["headers"]["subject"] == "Urgent payment needed"


def test_parse_eml_bytes():
    sample = b"Subject: Test message\nFrom: sender@example.com\nTo: user@example.com\n\nHello from the parser\n"

    parsed = parse_email_content(sample)

    assert parsed["subject"] == "Test message"
    assert parsed["from"] == "sender@example.com"
    assert parsed["body"].startswith("Hello from the parser")
