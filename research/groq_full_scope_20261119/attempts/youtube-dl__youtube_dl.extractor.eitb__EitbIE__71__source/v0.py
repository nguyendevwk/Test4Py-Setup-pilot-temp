import json
import pytest
from youtube_dl.extractor.eitb import EitbIE
from youtube_dl.utils import parse_iso8601

# Helper to create a minimal EitbIE instance with patched methods
def make_eitb_ie():
    ie = EitbIE()
    # Patch methods that would perform network I/O
    ie._download_json = lambda *args, **kwargs: {}
    ie._extract_m3u8_formats = lambda *args, **kwargs: []
    ie._extract_f4m_formats = lambda *args, **kwargs: []
    return ie

def test_basic_renditions(tmp_path):
    ie = make_eitb_ie()
    # Sample JSON with two renditions
    sample_json = {
        "web_media": [
            {
                "RENDITIONS": [
                    {"PMD_URL": "http://example.com/low.mp4", "ENCODING_RATE": "500", "FRAME_WIDTH": "640", "FRAME_HEIGHT": "360"},
                    {"PMD_URL": "http://example.com/high.mp4", "ENCODING_RATE": "1500", "FRAME_WIDTH": "1280", "FRAME_HEIGHT": "720"},
                ],
                "NAME_ES": "Test Video",
                "SHORT_DESC_ES": "A test description",
                "STILL_URL": "http://example.com/thumb.jpg",
                "LENGTH": "600000",
                "BROADCST_DATE": "2023-01-01 12:00:00",
                "TAGS": ["test", "video"],
            }
        ]
    }
    ie._download_json = lambda url, video_id, *args, **kwargs: sample_json
    result = ie._real_extract("http://www.eitb.tv/es/video/test/123/123456")
    assert result["id"] == "123456"
    assert result["title"] == "Test Video"
    assert result["description"] == "A test description"
    assert result["thumbnail"] == "http://example.com/thumb.jpg"
    assert result["duration"] == 600.0
    assert result["timestamp"] == parse_iso8601("2023-01-01 12:00:00", " ")
    assert result["tags"] == ["test", "video"]
    formats = result["formats"]
    assert len(formats) == 2
    assert formats[0]["url"] == "http://example.com/low.mp4"
    assert formats[0]["format_id"] == "http-500"
    assert formats[0]["width"] == 640
    assert formats[0]["height"] == 360
    assert formats[0]["tbr"] == 500.0
    assert formats[1]["format_id"] == "http-1500"

def test_hls_token_and_formats(tmp_path):
    ie = make_eitb_ie()
    sample_json = {
        "web_media": [
            {
                "RENDITIONS": [],
                "HLS_SURL": "http://example.com/stream.m3u8",
                "NAME_ES": "HLS Video",
                "SHORT_DESC_ES": "HLS test",
                "STILL_URL": "http://example.com/thumb2.jpg",
                "LENGTH": "300000",
                "BROADCST_DATE": "2023-02-02 10:00:00",
                "TAGS": ["hls"],
            }
        ]
    }
    # Return token data
    token_json = {"token": "abc123"}
    def download_json(url, video_id, *args, **kwargs):
        if "TokenAuth" in url:
            return token_json
        return sample_json
    ie._download_json = download_json
    # Simulate extraction of m3u8 formats
    ie._extract_m3u8_formats = lambda url, vid, **kw: [{"url": url, "format_id": "hls"}]
    result = ie._real_extract("http://www.eitb.tv/es/video/hls/456/456789")
    assert result["id"] == "456789"
    assert result["title"] == "HLS Video"
    assert result["formats"] == [{"url": "http://example.com/stream.m3u8?hdnts=abc123", "format_id": "hls"}]

def test_hds_and_no_renditions(tmp_path):
    ie = make_eitb_ie()
    sample_json = {
        "web_media": [
            {
                "RENDITIONS": [],
                "HDS_SURL": "http://example.com/stream.f4m",
                "NAME_ES": "HDS Video",
                "SHORT_DESC_ES": "HDS test",
                "STILL_URL": "http://example.com/thumb3.jpg",
                "LENGTH": "120000",
                "BROADCST_DATE": "2023-03-03 08:00:00",
                "TAGS": ["hds"],
            }
        ]
    }
    ie._download_json = lambda url, video_id, *args, **kwargs: sample_json
    ie._extract_f4m_formats = lambda url, vid, **kw: [{"url": url, "format_id": "hds"}]
    result = ie._real_extract("http://www.eitb.tv/es/video/hds/789/789012")
    assert result["id"] == "789012"
    assert result["title"] == "HDS Video"
    assert result["formats"] == [{"url": "http://example.com/stream.f4m?hdcore=3.7.0", "format_id": "hds"}]
