from app.analysis import analyzer


def test_header_analysis_extracts_received_chain():
    sample = """Subject: Warning
From: user@example.com
To: victim@example.com
Received: from mail.example.net by mx.example.org
Received: from suspicious-host.net by mail.example.net

Please verify your account.
"""

    result = analyzer.analyze(sample)

    assert result["header_analysis"]["received_count"] == 2
    assert result["header_analysis"]["has_multiple_received"] is True
    assert "mx.example.org" in result["header_analysis"]["origin_hosts"]
