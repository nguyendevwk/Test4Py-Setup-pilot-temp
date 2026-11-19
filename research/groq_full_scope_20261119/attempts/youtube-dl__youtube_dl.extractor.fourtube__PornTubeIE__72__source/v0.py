import re
import json
import base64
import pytest
from youtube_dl.extractor.fourtube import PornTubeIE


class DummyPornTubeIE(PornTubeIE):
    """Subclass that overrides network-dependent methods for testing."""

    def __init__(self, webpage, encoded_json, formats):
        super().__init__()
        self._webpage = webpage
        self._encoded_json = encoded_json
        self._formats = formats

    def _download_webpage(self, url, display_id):
        return self._webpage

    def _search_regex(self, pattern, string, name, group=None):
        # Return the encoded JSON string regardless of pattern
        return self._encoded_json

    def _extract_formats(self, url, video_id, media_id, sources):
        return self._formats


def build_webpage_with_initialstate(encoded_json):
    """Return a minimal webpage containing the INITIALSTATE assignment."""
    return f"""
    <html>
    <script>
    var INITIALSTATE = '{encoded_json}';
    </script>
    </html>
    """


def encode_json_to_initialstate(data):
    """Encode a dict to the base64-quoted string used by the extractor."""
    json_str = json.dumps(data)
    b64 = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    return b64


def test_porn_tube_normal_extraction():
    # Prepare fake video data
    video_data = {
        "page": {
            "video": {
                "title": "Test Video",
                "mediaId": "12345",
                "encodings": [
                    {"height": 720},
                    {"height": 480}
                ],
                "masterThumb": "https://example.com/thumb.jpg",
                "user": {"username": "Tester", "id": 42},
                "channel": {"name": "TestChannel", "id": 99},
                "likes": 100,
                "dislikes": 5,
                "playsQty": 1000,
                "durationInSeconds": 120,
                "publishedAt": "2023-01-01T00:00:00Z"
            }
        }
    }
    encoded_json = encode_json_to_initialstate(video_data)
    webpage = build_webpage_with_initialstate(encoded_json)
    dummy_formats = [{"format_id": "720p", "url": "http://example.com/720p.mp4"}]

    extractor = DummyPornTubeIE(webpage, encoded_json, dummy_formats)
    result = extractor._real_extract("https://www.porntube.com/videos/test_video_12345")

    assert result["id"] == "12345"
    assert result["title"] == "Test Video"
    assert result["formats"] == dummy_formats
    assert result["thumbnail"] == "https://example.com/thumb.jpg"
    assert result["uploader"] == "Tester"
    assert result["uploader_id"] == "42"
    assert result["channel"] == "TestChannel"
    assert result["channel_id"] == "99"
    assert result["like_count"] == 100
    assert result["dislike_count"] == 5
    assert result["view_count"] == 1000
    assert result["duration"] == 120
    assert result["age_limit"] == 18
    # Timestamp should be parsed correctly
    assert result["timestamp"] == 1672531200  # 2023-01-01T00:00:00Z in epoch


def test_porn_tube_missing_optional_fields():
    # Video data missing optional fields like user, channel, likes, etc.
    video_data = {
        "page": {
            "video": {
                "title": "No User Video",
                "mediaId": "67890",
                "encodings": [{"height": 360}],
                "masterThumb": None,
                # No user, channel, likes, dislikes, playsQty, durationInSeconds
                "publishedAt": "2022-12-31T23:59:59Z"
            }
        }
    }
    encoded_json = encode_json_to_initialstate(video_data)
    webpage = build_webpage_with_initialstate(encoded_json)
    dummy_formats = [{"format_id": "360p", "url": "http://example.com/360p.mp4"}]

    extractor = DummyPornTubeIE(webpage, encoded_json, dummy_formats)
    result = extractor._real_extract("https://www.porntube.com/videos/no_user_67890")

    assert result["id"] == "67890"
    assert result["title"] == "No User Video"
    assert result["formats"] == dummy_formats
    assert result["thumbnail"] is None
    # uploader should fallback to channel, both missing -> None
    assert result["uploader"] is None
    assert result["uploader_id"] is None
    assert result["channel"] is None
    assert result["channel_id"] is None
    assert result["like_count"] is None
    assert result["dislike_count"] is None
    assert result["view_count"] is None
    assert result["duration"] is None
    assert result["age_limit"] == 18
    assert result["timestamp"] == 1672531199  # 2022-12-31T23:59:59Z


def test_porn_tube_invalid_url_raises():
    # Use a URL that does not match the VALID_URL pattern
    extractor = PornTubeIE()
    with pytest.raises(AttributeError):
        # _real_extract expects a match; passing invalid URL triggers AttributeError
        extractor._real_extract("https://www.invalid.com/videos/123")
