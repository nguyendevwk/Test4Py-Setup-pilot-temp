import json
import pytest
from youtube_dl.extractor.eitb import EitbIE
from youtube_dl.utils import sanitized_Request

class FakeEitbIE(EitbIE):
    """EitbIE with overridden network methods for testing."""
    def __init__(self, json_response, token_response=None):
        super().__init__()
        self._json_response = json_response
        self._token_response = token_response

    def _download_json(self, url, video_id, note=None, **kw):
        # Return the prepared JSON response regardless of URL
        if isinstance(url, sanitized_Request):
            return self._token_response
        return self._json_response


def test_basic_extraction(tmp_path):
    # Prepare a minimal JSON response with one rendition and HLS
    video_id = "1234567890"
    json_response = {
        "web_media": [
            {
                "RENDITIONS": [
                    {
                        "PMD_URL": "http://example.com/video.mp4",
                        "ENCODING_RATE": "1500",
                        "FRAME_WIDTH": "1280",
                        "FRAME_HEIGHT": "720",
                    }
                ],
                "HLS_SURL": "http://example.com/playlist.m3u8",
                "NAME_ES": "Test Video",
                "SHORT_DESC_ES": "A test description",
                "STILL_URL": "http://example.com/thumb.jpg",
                "LENGTH": "600000",
                "BROADCST_DATE": "2023-01-01 12:00:00",
                "TAGS": ["test", "video"],
            }
        ],
        "desc_group": "Group description",
    }
    token_response = {"token": "abc123"}

    ie = FakeEitbIE(json_response, token_response)
    result = ie._real_extract(f"http://www.eitb.tv/es/video/test/{video_id}")

    assert result["id"] == video_id
    assert result["title"] == "Test Video"
    assert result["description"] == "A test description"
    assert result["thumbnail"] == "http://example.com/thumb.jpg"
    assert result["duration"] == 600.0
    assert result["timestamp"] == 1672574400  # 2023-01-01 12:00:00 UTC
    assert result["tags"] == ["test", "video"]
    formats = result["formats"]
    assert any(f["url"] == "http://example.com/video.mp4" for f in formats)
    assert any(f["url"].startswith("http://example.com/playlist.m3u8") for f in formats)


def test_no_renditions(tmp_path):
    # JSON with no renditions but with HDS
    video_id = "9876543210"
    json_response = {
        "web_media": [
            {
                "RENDITIONS": [],
                "HDS_SURL": "http://example.com/stream.f4m",
                "NAME_EU": "HDS Video",
                "SHORT_DESC_EU": "HDS description",
                "THUMBNAIL_URL": "http://example.com/hds_thumb.jpg",
                "LENGTH": "300000",
                "BROADCST_DATE": "2022-12-31 23:59:59",
                "TAGS": ["hds"],
            }
        ],
        "desc_group": "Group description",
    }

    ie = FakeEitbIE(json_response)
    result = ie._real_extract(f"http://www.eitb.tv/es/video/test/{video_id}")

    assert result["id"] == video_id
    assert result["title"] == "HDS Video"
    assert result["description"] == "HDS description"
    assert result["thumbnail"] == "http://example.com/hds_thumb.jpg"
    assert result["duration"] == 300.0
    assert result["tags"] == ["hds"]
    # No HTTP format should be present
    assert all("http" not in f["format_id"] for f in result["formats"])


def test_missing_token(tmp_path):
    # JSON with HLS but token endpoint returns None
    video_id = "5555555555"
    json_response = {
        "web_media": [
            {
                "RENDITIONS": [
                    {
                        "PMD_URL": "http://example.com/video.mp4",
                        "ENCODING_RATE": "800",
                        "FRAME_WIDTH": "640",
                        "FRAME_HEIGHT": "360",
                    }
                ],
                "HLS_SURL": "http://example.com/playlist.m3u8",
                "NAME_ES": "No Token Video",
                "SHORT_DESC_ES": "No token description",
                "STILL_URL": "http://example.com/thumb.jpg",
                "LENGTH": "120000",
                "BROADCST_DATE": "2021-06-15 10:00:00",
                "TAGS": ["no", "token"],
            }
        ],
        "desc_group": "Group description",
    }

    ie = FakeEitbIE(json_response, token_response=None)
    result = ie._real_extract(f"http://www.eitb.tv/es/video/test/{video_id}")

    assert result["id"] == video_id
    assert result["title"] == "No Token Video"
    assert result["description"] == "No token description"
    assert result["thumbnail"] == "http://example.com/thumb.jpg"
    assert result["duration"] == 120.0
    assert result["tags"] == ["no", "token"]
    # HLS formats should not be added because token is missing
    assert all("hls" not in f.get("format_id", "") for f in result["formats"])
