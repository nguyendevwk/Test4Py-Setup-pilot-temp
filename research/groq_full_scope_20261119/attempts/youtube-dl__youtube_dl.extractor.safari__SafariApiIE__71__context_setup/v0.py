import re
import pytest
from youtube_dl.extractor.safari import SafariApiIE


def test_safari_api_ie_normal(monkeypatch, tmp_path):
    """Test normal extraction returns correct URL result."""
    # Prepare a fake JSON response with a web_url field
    fake_json = {"web_url": "https://example.com/video.mp4"}
    # Monkeypatch the _download_json method to return the fake JSON
    monkeypatch.setattr(
        SafariApiIE,
        "_download_json",
        lambda self, url, video_id, note: fake_json,
    )
    # Instantiate the extractor
    ie = SafariApiIE()
    # Use a valid URL from the tests
    url = "https://www.safaribooksonline.com/api/v1/book/9780133392838/chapter/part00.html"
    result = ie._real_extract(url)
    # The result should be a URLResult pointing to the fake web_url
    assert result.url == fake_json["web_url"]
    assert result.ie_key() == "SafariIE"


def test_safari_api_ie_invalid_url(monkeypatch):
    """Test that an invalid URL raises an AttributeError due to missing match."""
    ie = SafariApiIE()
    # Provide a URL that does not match the pattern
    invalid_url = "https://www.example.com/notmatching"
    with pytest.raises(AttributeError):
        ie._real_extract(invalid_url)


def test_safari_api_ie_missing_web_url(monkeypatch):
    """Test that missing 'web_url' in JSON raises a KeyError."""
    # Return JSON without the required key
    monkeypatch.setattr(
        SafariApiIE,
        "_download_json",
        lambda self, url, video_id, note: {"not_web_url": "value"},
    )
    ie = SafariApiIE()
    url = "https://www.safaribooksonline.com/api/v1/book/9780133392838/chapter/part00.html"
    with pytest.raises(KeyError):
        ie._real_extract(url)
