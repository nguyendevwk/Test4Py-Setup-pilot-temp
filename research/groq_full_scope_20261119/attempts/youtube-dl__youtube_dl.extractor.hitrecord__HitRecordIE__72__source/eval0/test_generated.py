import pytest
from youtube_dl.extractor.hitrecord import HitRecordIE
from youtube_dl.utils import clean_html

def test_valid_url_match():
    """Ensure the extractor correctly extracts the video id from a valid URL."""
    url = "https://hitrecord.org/records/1234567"
    extractor = HitRecordIE()
    # _match_id should return the numeric id part
    assert extractor._match_id(url) == "1234567"

def test_tags_extraction(monkeypatch):
    """Verify that tags are extracted only when present and correctly filtered."""
    # Prepare a fake JSON response with tags
    fake_video = {
        "title": "Test Video",
        "source_url": {"mp4_url": "https://example.com/video.mp4"},
        "body": "<p>Desc</p>",
        "duration": 120000,
        "created_at_i": 1609459200,
        "user": {"username": "tester", "id": 42},
        "total_views_count": 100,
        "hearts_count": 10,
        "comments_count": 5,
        "tags": [
            {"text": "fun"},
            {"text": None},
            {"text": 123},
            {"not_text": "ignore"},
        ],
    }

    # Monkeypatch the network call to return our fake data
    monkeypatch.setattr(
        HitRecordIE,
        "_download_json",
        lambda self, url, video_id: fake_video,
    )

    extractor = HitRecordIE()
    result = extractor._real_extract("https://hitrecord.org/records/9999999")

    # Only the valid string tag should be present
    assert result["tags"] == ["fun"]
    # Verify other fields are correctly parsed
    assert result["id"] == "9999999"
    assert result["url"] == "https://example.com/video.mp4"
    assert result["title"] == "Test Video"
    assert result["description"] == "Desc"
    assert result["duration"] == 120.0
    assert result["timestamp"] == 1609459200
    assert result["uploader"] == "tester"
    assert result["uploader_id"] == "42"
    assert result["view_count"] == 100
    assert result["like_count"] == 10
    assert result["comment_count"] == 5

def test_missing_optional_fields(monkeypatch):
    """Ensure that missing optional fields are handled gracefully."""
    # Fake JSON with minimal required fields and missing optional ones
    fake_video = {
        "title": "Minimal",
        "source_url": {"mp4_url": "https://example.com/minimal.mp4"},
        "body": None,
        "duration": None,
        "created_at_i": None,
        "user": {"username": None, "id": None},
        "total_views_count": None,
        "hearts_count": None,
        "comments_count": None,
        "tags": None,
    }

    monkeypatch.setattr(
        HitRecordIE,
        "_download_json",
        lambda self, url, video_id: fake_video,
    )

    extractor = HitRecordIE()
    result = extractor._real_extract("https://hitrecord.org/records/1")

    # Optional fields should be None or empty
    assert result["tags"] is None
    assert result["description"] == ""
    assert result["duration"] is None
    assert result["timestamp"] is None
    assert result["uploader"] is None
    assert result["uploader_id"] is None
    assert result["view_count"] is None
    assert result["like_count"] is None
    assert result["comment_count"] is None
