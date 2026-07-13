from app.url_analyzer import url_analyzer


def test_url_analyzer_flags_shortened_and_http_urls():
    urls = ["http://example.com", "https://bit.ly/abc123"]

    result = url_analyzer.analyze(urls)

    assert len(result) == 2
    assert result[0]["is_suspicious"] is True
    assert result[1]["is_shortened"] is True
    assert any("URL acortada" in item["risk_reason"] for item in result)
