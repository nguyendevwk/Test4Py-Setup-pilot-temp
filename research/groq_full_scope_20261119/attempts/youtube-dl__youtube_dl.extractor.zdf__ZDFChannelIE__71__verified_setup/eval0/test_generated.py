import pytest
from youtube_dl.extractor.zdf import ZDFChannelIE


@pytest.fixture
def ie():
    """Instantiate ZDFChannelIE with a dummy downloader."""
    return ZDFChannelIE(None)


def test_real_extract_parses_multiple_entries(ie, monkeypatch):
    """_real_extract should return a playlist with all unique data-plusbar-url entries."""
    # Prepare a fake webpage containing two URLs, one duplicated
    fake_webpage = """
        <html>
            <body>
                <div data-plusbar-url="https://player.zdf.de/video1.html"></div>
                <div data-plusbar-url="https://player.zdf.de/video2.html"></div>
                <div data-plusbar-url="https://player.zdf.de/video1.html"></div>
            </body>
        </html>
    """
    # Monkeypatch the download method and title search
    monkeypatch.setattr(ie, "_download_webpage", lambda url, video_id: fake_webpage)
    monkeypatch.setattr(ie, "_og_search_title", lambda webpage, fatal=False: "Fake Title")

    result = ie._real_extract("https://www.zdf.de/some/channel")

    # The playlist should contain two unique entries
    assert isinstance(result, dict)
    assert result["id"] == "channel"
    assert result["title"] == "Fake Title"
    assert len(result["entries"]) == 2
    urls = {entry["url"] for entry in result["entries"]}
    assert urls == {
        "https://player.zdf.de/video1.html",
        "https://player.zdf.de/video2.html",
    }


def test_real_extract_no_entries(ie, monkeypatch):
    """When no data-plusbar-url is found, the playlist should be empty."""
    fake_webpage = "<html><body>No video links here.</body></html>"
    monkeypatch.setattr(ie, "_download_webpage", lambda url, video_id: fake_webpage)
    monkeypatch.setattr(ie, "_og_search_title", lambda webpage, fatal=False: "No Videos")

    result = ie._real_extract("https://www.zdf.de/empty/channel")

    assert isinstance(result, dict)
    assert result["id"] == "channel"
    assert result["title"] == "No Videos"
    assert result["entries"] == []


def test_real_extract_invalid_url(ie, monkeypatch):
    """_real_extract should raise a ValueError if the URL does not match the pattern."""
    # Monkeypatch _download_webpage to avoid network call
    monkeypatch.setattr(ie, "_download_webpage", lambda url, video_id: "<html></html>")

    # URL that does not match the regex should cause a ValueError from _match_id
    with pytest.raises(ValueError):
        ie._real_extract("https://www.example.com/notmatching")
