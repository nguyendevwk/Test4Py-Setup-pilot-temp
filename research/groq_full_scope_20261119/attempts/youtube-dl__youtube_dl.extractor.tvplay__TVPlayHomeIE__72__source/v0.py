import re
import pytest
from youtube_dl.extractor.tvplay import TVPlayHomeIE
from youtube_dl.utils import parse_duration, int_or_none


def test_valid_url_matches():
    """The _VALID_URL regex should match a known URL and capture the id."""
    url = "https://tvplay.tv3.lt/aferistai-n-7/aferistai-10047125/"
    match = re.match(TVPlayHomeIE._VALID_URL, url)
    assert match is not None, "URL did not match the regex"
    assert match.group("id") == "10047125", "Captured id is incorrect"


def test_real_extract_with_image(monkeypatch, tmp_path):
    """_real_extract should return expected keys when imageUrl is present."""
    # Prepare a fake asset JSON
    fake_asset = {
        "movie": {"contentUrl": "http://example.com/stream.m3u8"},
        "assetId": "12345",
        "title": {"title": "Test Video", "summaryLong": "Long summary"},
        "imageUrl": "/images/test.jpg",
        "metadata": {"seasonNumber": "2", "episodeNumber": "5"},
        "tvSeriesTitle": "Test Series",
        "tvSeasonTitle": "Season 2",
        "runTime": "PT7M30S",
        "titleBrief": "Brief Title",
    }

    # Monkeypatch _download_json to return the fake asset
    def fake_download_json(url, video_id):
        assert url.endswith(f"/sb/public/asset/{video_id}")
        return fake_asset

    ie = TVPlayHomeIE()
    monkeypatch.setattr(ie, "_download_json", fake_download_json)

    # Monkeypatch _extract_m3u8_formats to return a dummy format list
    def fake_extract_m3u8_formats(url, video_id, ext, fmt, m3u8_id):
        return [{"url": url, "format_id": "hls"}]

    monkeypatch.setattr(ie, "_extract_m3u8_formats", fake_extract_m3u8_formats)

    result = ie._real_extract("https://tvplay.tv3.lt/aferistai-10047125/")

    assert result["id"] == "12345"
    assert result["title"] == "Test Video"
    assert result["description"] == "Long summary"
    assert result["thumbnails"] == [
        {"url": "https://tvplay.tv3.lt/images/test.jpg", "ext": "jpg"}
    ]
    assert result["duration"] == 450  # 7 minutes 30 seconds
    assert result["series"] == "Test Series"
    assert result["season"] == "Season 2"
    assert result["season_number"] == 2
    assert result["episode"] == "Brief Title"
    assert result["episode_number"] == 5
    assert result["formats"] == [{"url": "http://example.com/stream.m3u8", "format_id": "hls"}]


def test_real_extract_without_image(monkeypatch):
    """_real_extract should handle missing imageUrl gracefully."""
    fake_asset = {
        "movie": {"contentUrl": "http://example.com/stream.m3u8"},
        "assetId": "67890",
        "title": {"title": "No Image Video", "summaryShort": "Short summary"},
        "metadata": {"seasonNumber": None, "episodeNumber": None},
        "tvSeriesTitle": None,
        "tvSeasonTitle": None,
        "runTime": None,
        "titleBrief": None,
    }

    def fake_download_json(url, video_id):
        return fake_asset

    ie = TVPlayHomeIE()
    monkeypatch.setattr(ie, "_download_json", fake_download_json)

    def fake_extract_m3u8_formats(url, video_id, ext, fmt, m3u8_id):
        return [{"url": url, "format_id": "hls"}]

    monkeypatch.setattr(ie, "_extract_m3u8_formats", fake_extract_m3u8_formats)

    result = ie._real_extract("https://tvplay.tv3.lt/no-image-67890/")

    assert result["id"] == "67890"
    assert result["title"] == "No Image Video"
    assert result["description"] == "Short summary"
    assert result["thumbnails"] is None
    assert result["duration"] is None
    assert result["series"] is None
    assert result["season"] is None
    assert result["season_number"] is None
    assert result["episode"] is None
    assert result["episode_number"] is None
    assert result["formats"] == [{"url": "http://example.com/stream.m3u8", "format_id": "hls"}]
