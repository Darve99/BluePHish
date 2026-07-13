from app.analysis import analyzer


def test_analyzer_extracts_headers_and_urls():
    sample = """Subject: Billing issue
From: support@paypal-security.com
To: user@example.com
Reply-To: help@paypal.com
Return-Path: <bounce@paypal-security.com>

Please verify your account: https://bit.ly/abc123
"""

    result = analyzer.analyze(sample)

    assert result["subject"] == "Billing issue"
    assert result["from"] == "support@paypal-security.com"
    assert result["reply_to"] == "help@paypal.com"
    assert result["return_path"] == "bounce@paypal-security.com"
    assert "https://bit.ly/abc123" in result["urls"]
    assert result["score"] >= 20
