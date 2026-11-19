import base64
import json
import re
import pytest
from youtube_dl.extractor.fourtube import PornTubeIE


def _make_webpage(json_obj):
    """Return a webpage string containing an INITIALSTATE base64 value."""
    json_str = json.dumps(json_obj, separators=(',', ':'))
    b64 = base64.b64encode(json_str.encode('utf-8')).decode('ascii')
    return f"<html><body>INITIALSTATE='{b64}'</body></html>"


def test_porn_tube_extract_basic(tmp_path):
    """Test normal extraction with all fields present."""
    # Prepare a minimal JSON structure expected by the extractor
    video_json = {
        "page": {
            "video": {
                "title": "Test Video",
                "mediaId": "123",
                "encodings": [{"height": "720"}, {"height": "480"}],
                "masterThumb": "http://thumb.jpg",
                "user": {"username": "Tester", "id": 42},
                "channel": {"name": "TestChannel", "id": 99},
                "likes": 10,
                "dislikes": 2,
                "playsQty": 1000,
                "durationInSeconds": 120,
                "publishedAt": "2023-01-01T00:00:00Z",
            }
        }
    }

    webpage = _make_webpage(video_json)

    ie = PornTubeIE()
    # Patch methods that would otherwise perform network I/O
    ie._download_webpage = lambda url, display_id: webpage
    ie._extract_formats = lambda url, vid, mid, src: [{"format_id": "720p"}]

    result = ie._real_extract("https://www.porntube.com/videos/test_123")

    assert result["id"] == "123"
    assert result["title"] == "Test Video"
    assert result["formats"] == [{"format_id": "720p"}]
    assert result["thumbnail"] == "http://thumb.jpg"
    assert result["uploader"] == "Tester"
    assert result["uploader_id"] == "42"
    assert result["channel"] == "TestChannel"
    assert result["channel_id"] == "99"
    assert result["like_count"] == 10
    assert result["dislike_count"] == 2
    assert result["view_count"] == 1000
    assert result["duration"] == 120
    assert result["age_limit"] == 18
    # timestamp should be a valid Unix timestamp
    assert isinstance(result["timestamp"], int)


def test_porn_tube_extract_missing_optional(tmp_path):
    """Test extraction when optional user/channel fields are missing."""
    video_json = {
        "page": {
            "video": {
                "title": "No User Video",
                "mediaId": "456",
                "encodings": [{"height": "360"}],
                "masterThumb": None,
                # No user or channel keys
                "likes": None,
                "dislikes": None,
                "playsQty": None,
                "durationInSeconds": None,
                "publishedAt": None,
            }
        }
    }

    webpage = _make_webpage(video_json)

    ie = PornTubeIE()
    ie._download_webpage = lambda url, display_id: webpage
    ie._extract_formats = lambda url, vid, mid, src: [{"format_id": "360p"}]

    result = ie._real_extract("https://www.porntube.com/videos/no_user_456")

    assert result["uploader"] is None
    assert result["uploader_id"] is None
    assert result["channel"] is None
    assert result["channel_id"] is None
    assert result["like_count"] is None
    assert result["dislike_count"] is None
    assert result["view_count"] is None
    assert result["duration"] is None
    assert result["thumbnail"] is None
    assert result["timestamp"] is None


def test_porn_tube_extract_invalid_url():
    """Test that an invalid URL raises an AttributeError due to regex mismatch."""
    ie = PornTubeIE()
    with pytest.raises(AttributeError):
        ie._real_extract("https://example.com/invalid/url")
