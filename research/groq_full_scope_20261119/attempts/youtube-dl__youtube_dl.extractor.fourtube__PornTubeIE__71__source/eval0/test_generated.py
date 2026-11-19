import re
import json
import pytest
from youtube_dl.extractor.fourtube import PornTubeIE
from youtube_dl.utils import int_or_none, unified_timestamp

# Helper to create a fake webpage containing the INITIALSTATE JSON
def _make_webpage(video_json):
    encoded = json.dumps(video_json).encode("utf-8")
    import base64
    b64 = base64.b64encode(encoded).decode("utf-8")
    return f"some html before INITIALSTATE='{b64}' some html after"

def _patch_methods(ie, webpage, json_data):
    # Patch _download_webpage to return our fake webpage
    ie._download_webpage = lambda url, display_id: webpage
    # Patch _search_regex to return the encoded JSON string
    ie._search_regex = lambda pattern, text, name, group=None: json_data
    # Patch _extract_formats to return a deterministic list
    ie._extract_formats = lambda url, vid, mid, srcs: [
        {"format_id": f"{h}p", "height": int(h)} for h in srcs
    ]

def test_porn_tube_normal_extraction():
    ie = PornTubeIE()
    video_id = "1234567"
    display_id = "test-video"
    # Build a minimal video JSON
    video_json = {
        "page": {
            "video": {
                "title": "Test Video",
                "mediaId": "media123",
                "encodings": [
                    {"height": "720"},
                    {"height": "480"},
                ],
                "masterThumb": "https://thumb.url/image.jpg",
                "user": {"username": "UploaderName", "id": 42},
                "channel": {"name": "ChannelName", "id": 99},
                "likes": 100,
                "dislikes": 5,
                "playsQty": 2000,
                "durationInSeconds": 300,
                "publishedAt": "2023-01-01T12:00:00Z",
            }
        }
    }
    webpage = _make_webpage(video_json)
    json_data = json.dumps(video_json).encode("utf-8")
    import base64
    b64 = base64.b64encode(json_data).decode("utf-8")
    _patch_methods(ie, webpage, b64)

    result = ie._real_extract(f"https://www.porntube.com/videos/test-video_{video_id}")

    assert result["id"] == video_id
    assert result["title"] == "Test Video"
    assert result["uploader"] == "UploaderName"
    assert result["uploader_id"] == "42"
    assert result["channel"] == "ChannelName"
    assert result["channel_id"] == "99"
    assert result["like_count"] == 100
    assert result["dislike_count"] == 5
    assert result["view_count"] == 2000
    assert result["duration"] == 300
    assert result["thumbnail"] == "https://thumb.url/image.jpg"
    assert result["age_limit"] == 18
    # Formats should contain two entries with correct format_id
    format_ids = {f["format_id"] for f in result["formats"]}
    assert format_ids == {"720p", "480p"}

def test_porn_tube_missing_optional_fields():
    ie = PornTubeIE()
    video_id = "7654321"
    display_id = "missing-fields"
    video_json = {
        "page": {
            "video": {
                "title": "No Optional",
                "mediaId": "media456",
                "encodings": [
                    {"height": "360"},
                ],
                # No masterThumb, user, channel, likes, dislikes, playsQty, durationInSeconds, publishedAt
            }
        }
    }
    webpage = _make_webpage(video_json)
    json_data = json.dumps(video_json).encode("utf-8")
    import base64
    b64 = base64.b64encode(json_data).decode("utf-8")
    _patch_methods(ie, webpage, b64)

    result = ie._real_extract(f"https://www.porntube.com/videos/{display_id}_{video_id}")

    assert result["id"] == video_id
    assert result["title"] == "No Optional"
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
    assert result["formats"] == [{"format_id": "360p", "height": 360}]

def test_porn_tube_invalid_regex_raises():
    ie = PornTubeIE()
    # Patch _download_webpage to return a page without the INITIALSTATE string
    ie._download_webpage = lambda url, display_id: "<html>No data</html>"
    # _search_regex will raise a regex error because pattern not found
    ie._search_regex = lambda pattern, text, name, group=None: re.search(pattern, text).group("value")
    with pytest.raises(AttributeError):
        ie._real_extract("https://www.porntube.com/videos/invalid_0000000")
