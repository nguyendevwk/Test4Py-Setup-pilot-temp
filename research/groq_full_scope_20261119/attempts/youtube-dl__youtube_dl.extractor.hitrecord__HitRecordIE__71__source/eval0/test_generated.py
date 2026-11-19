import pytest
from youtube_dl.extractor.hitrecord import HitRecordIE
from youtube_dl.utils import clean_html

class DummyHitRecordIE(HitRecordIE):
    """Subclass that overrides _download_json to return a controlled payload."""
    def __init__(self, payload):
        super().__init__()
        self._payload = payload

    def _download_json(self, url, video_id, *args, **kwargs):
        return self._payload


def test_normal_extraction(tmp_path):
    # Payload mimicking a typical API response
    payload = {
        "title": "Test Video",
        "source_url": {"mp4_url": "https://example.com/video.mp4"},
        "body": "<p>Some <b>description</b></p>",
        "duration": 123456,  # milliseconds
        "created_at_i": 1609459200,
        "user": {"username": "tester", "id": 42},
        "total_views_count": 1000,
        "hearts_count": 200,
        "comments_count": 30,
        "tags": [{"text": "tag1"}, {"text": "tag2"}],
    }
    ie = DummyHitRecordIE(payload)
    result = ie._real_extract("https://hitrecord.org/records/12345")

    assert result["id"] == "12345"
    assert result["url"] == "https://example.com/video.mp4"
    assert result["title"] == "Test Video"
    assert result["description"] == "Some description"
    assert result["duration"] == 123.456
    assert result["timestamp"] == 1609459200
    assert result["uploader"] == "tester"
    assert result["uploader_id"] == "42"
    assert result["view_count"] == 1000
    assert result["like_count"] == 200
    assert result["comment_count"] == 30
    assert result["tags"] == ["tag1", "tag2"]


def test_missing_tags_and_optional_fields(tmp_path):
    # Payload with no tags and missing optional numeric fields
    payload = {
        "title": "No Tags Video",
        "source_url": {"mp4_url": "https://example.com/no_tags.mp4"},
        "body": "<p>No tags here</p>",
        "duration": None,
        "created_at_i": None,
        "user": {"username": "no_tags_user", "id": 99},
        "total_views_count": None,
        "hearts_count": None,
        "comments_count": None,
        "tags": [],
    }
    ie = DummyHitRecordIE(payload)
    result = ie._real_extract("https://hitrecord.org/records/67890")

    assert result["tags"] is None
    assert result["duration"] is None
    assert result["timestamp"] is None
    assert result["view_count"] is None
    assert result["like_count"] is None
    assert result["comment_count"] is None
    assert result["uploader"] == "no_tags_user"
    assert result["uploader_id"] == "99"


def test_invalid_url_raises_value_error():
    # The extractor should raise a ValueError when the URL does not match the pattern
    ie = HitRecordIE()
    with pytest.raises(ValueError):
        ie._real_extract("https://example.com/not_a_hitrecord_url")
