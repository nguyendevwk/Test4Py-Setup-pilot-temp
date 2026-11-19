import re
import pytest
from youtube_dl.extractor.zdf import ZDFChannelIE


@pytest.fixture
def ie():
    """Instantiate ZDFChannelIE with a dummy downloader."""
    return ZDFChannelIE(downloader=None)


def test_real_extract_parses_multiple_entries(monkeypatch, ie):
    """_real_extract should return a playlist with all unique data-plusbar-url entries."""
    # Prepare a fake webpage containing two distinct URLs and one duplicate
    fake_webpage = (
        '<div data-plusbar-url="https://player.zdf.de/video1.html"></div>'
        '<div data-plusbar-url="https://player.zdf.de/video2.html"></div>'
        '<div data-plusbar-url="https://player.zdf.de/video1.html"></div>'
    )
    # Monkeypatch the download method to return our fake webpage
    monkeypatch.setattr(ie, "_download_webpage", lambda url, video_id: fake_webpage)

    # Call the extractor
    result = ie._real_extract("https://www.zdf.de/some/channel")

    # The result should be a playlist dict
    assert isinstance(result, dict)
    assert result["entries"] is not None
    # Two unique URLs should be present
    urls = [entry["url"] for entry in result["entries"]]
    assert set(urls) == {
        "https://player.zdf.de/video1.html",
        "https://player.zdf.de/video2.html",
    }
    # Each entry should be a result for ZDFIE
    for entry in result["entries"]:
        assert entry["ie"] == "ZDFIE"


def test_real_extract_no_entries(monkeypatch, ie):
    """If no data-plusbar-url is found, the playlist should be empty."""
    fake_webpage = '<div>No relevant URLs here</div>'
    monkeypatch.setattr(ie, "_download_webpage", lambda url, video_id: fake_webpage)

    result = ie._real_extract("https://www.zdf.de/empty/channel")

    assert isinstance(result, dict)
    assert result["entries"] == []


def test_real_extract_invalid_url(monkeypatch, ie):
    """_real_extract should raise a ValueError when the URL does not match the pattern."""
    # Monkeypatch the download method to avoid network call
    monkeypatch.setattr(ie, "_download_webpage", lambda url, video_id: "")

    # URL that does not match the VALID_URL regex
    with pytest.raises(ValueError):
        ie._real_extract("https://example.com/not/zdf")
