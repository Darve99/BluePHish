from app.analysis import analyzer


def test_auth_headers_are_detected():
    sample = """Subject: Security alert
From: bad@example.com
To: user@example.com
Authentication-Results: spf=fail; dkim=fail; dmarc=fail

Please verify your password immediately.
"""

    result = analyzer.analyze(sample)

    assert result["auth_results"]["spf"] == "fail"
    assert result["auth_results"]["dkim"] == "fail"
    assert result["auth_results"]["dmarc"] == "fail"
    assert result["score"] >= 60
