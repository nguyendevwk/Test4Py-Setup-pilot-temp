import pytest
from youtube_dl.extractor.eitb import EitbIE
from youtube_dl.utils import sanitized_Request

class DummyEitbIE(EitbIE):
    """EitbIE subclass that returns predefined JSON data instead of downloading."""
    def __init__(self, json_data, token_data=None):
        super().__init__()
        self._json_data = json_data
        self._token_data = token_data

    def _download_json(self, url, video_id, note=None, fatal=True, headers=None):
        # Return the predefined JSON data for the video request
        if 'ServiceMultiweb/Video/MULTIWEBTV' in url:
            return self._json_data
        # Return the predefined token data for the auth request
        if 'TokenAuth' in url:
            return self._token_data
        raise ValueError(f"Unexpected URL: {url}")

def test_normal_extraction(tmp_path):
    # Sample JSON mimicking the real API response
    video_json = {
        "web_media": [
            {
                "RENDITIONS": [
                    {
                        "PMD_URL": "http://example.com/video1.mp4",
                        "ENCODING_RATE": "1500",
                        "FRAME_WIDTH": "1280",
                        "FRAME_HEIGHT": "720"
                    },
                    {
                        "PMD_URL": "http://example.com/video2.mp4",
                        "ENCODING_RATE": "2500",
                        "FRAME_WIDTH": "1920",
                        "FRAME_HEIGHT": "1080"
                    }
                ],
                "HLS_SURL": "http://example.com/playlist.m3u8",
                "HDS_SURL": "http://example.com/stream.f4m",
                "NAME_ES": "Test Video",
                "SHORT_DESC_ES": "A test description",
                "STILL_URL": "http://example.com/thumb.jpg",
                "LENGTH": "600000",
                "BROADCST_DATE": "2023-01-01 12:00:00",
                "TAGS": ["test", "video"]
            }
        ]
    }
    token_json = {"token": "dummy_token"}
    extractor = DummyEitbIE(video_json, token_json)
    result = extractor._real_extract(
        "http://www.eitb.tv/es/video/test/123456/1234567890/"
    )
    assert result["id"] == "1234567890"
    assert result["title"] == "Test Video"
    assert result["description"] == "A test description"
    assert result["thumbnail"] == "http://example.com/thumb.jpg"
    assert result["duration"] == 600.0
    assert result["timestamp"] == 1672574400  # 2023-01-01 12:00:00 UTC
    assert result["tags"] == ["test", "video"]
    # Check that formats include the two renditions and the HLS/HDS formats
    format_ids = {f["format_id"] for f in result["formats"]}
    assert "http-1500" in format_ids
    assert "http-2500" in format_ids
    assert any(f["format_id"].startswith("hls") for f in result["formats"])
    assert any(f["format_id"].startswith("hds") for f in result["formats"])

def test_missing_rendition_url(tmp_path):
    # JSON with a rendition missing PMD_URL should be skipped
    video_json = {
        "web_media": [
            {
                "RENDITIONS": [
                    {"PMD_URL": None, "ENCODING_RATE": "1500"},
                    {"PMD_URL": "http://example.com/video.mp4", "ENCODING_RATE": "1500"}
                ],
                "NAME_ES": "Video",
                "SHORT_DESC_ES": "Desc",
                "STILL_URL": None,
                "LENGTH": "300000",
                "BROADCST_DATE": "2023-01-01 00:00:00",
                "TAGS": []
            }
        ]
    }
    extractor = DummyEitbIE(video_json)
    result = extractor._real_extract(
        "http://www.eitb.tv/es/video/test/123456/1234567890/"
    )
    # Only one format should be present
    assert len(result["formats"]) == 1
    assert result["formats"][0]["url"] == "http://example.com/video.mp4"

def test_invalid_url_raises():
    extractor = EitbIE()
    # URL that does not match the regex should raise a ValueError
    with pytest.raises(ValueError):
        extractor._match_id("http://invalid.url/notmatching")
