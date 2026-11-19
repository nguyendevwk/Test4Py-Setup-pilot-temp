import re
import json
import pytest
from youtube_dl.extractor.konserthusetplay import KonserthusetPlayIE

# Helper to create a minimal IE instance with overridden download methods
def make_ie(monkeypatch, webpage=None, json_data=None):
    ie = KonserthusetPlayIE()
    # Override _download_webpage to return the provided webpage
    monkeypatch.setattr(
        ie, "_download_webpage",
        lambda url, video_id: webpage or ""
    )
    # Override _download_json to return the provided json_data
    monkeypatch.setattr(
        ie, "_download_json",
        lambda url, video_id, transform_source=None: json_data or {}
    )
    return ie

def test_valid_url_parsing(monkeypatch):
    """Ensure that the extractor correctly extracts the video id from a valid URL."""
    url = "http://www.konserthusetplay.se/?m=CKDDnlCY-dhWAAqiMERd-A"
    ie = make_ie(monkeypatch, webpage="dummy")
    video_id = ie._match_id(url)
    assert video_id == "CKDDnlCY-dhWAAqiMERd-A"

def test_format_extraction_m3u8(monkeypatch):
    """Test that an m3u8 source URL is correctly parsed into formats."""
    # Minimal webpage containing the 'e' parameter
    webpage = (
        '... <script>var e="abc123";</script> ...'
    )
    # JSON returned by the rest endpoint
    json_data = {
        "media": {
            "playerconfig": {
                "playlist": [
                    {
                        "url": "http://example.com/stream_h264m.mp4",
                        "fallbackUrl": "http://fallback.com/video_h264m.mp4",
                        "bitrates": [],
                        "captionsAvailableLanguages": {}
                    }
                ]
            }
        }
    }
    ie = make_ie(monkeypatch, webpage=webpage, json_data=json_data)
    result = ie._real_extract("http://www.konserthusetplay.se/?m=CKDDnlCY-dhWAAqiMERd-A")
    # The extractor should produce at least one format with ext 'mp4'
    formats = result["formats"]
    assert any(f.get("ext") == "mp4" for f in formats)
    # The fallback URL should be present in the formats list
    assert any(f.get("url") == "http://fallback.com/video_h264m.mp4" for f in formats)

def test_subtitles_parsing(monkeypatch):
    """Verify that subtitles are extracted correctly from the source captions dict."""
    webpage = '... <script>var e="xyz";</script> ...'
    json_data = {
        "media": {
            "playerconfig": {
                "playlist": [
                    {
                        "captionsAvailableLanguages": {
                            "en": "http://captions.com/en.srt",
                            "none": "http://captions.com/none.srt",
                            "sv": "http://captions.com/sv.srt"
                        }
                    }
                ]
            }
        }
    }
    ie = make_ie(monkeypatch, webpage=webpage, json_data=json_data)
    result = ie._real_extract("http://rspoplay.se/?m=elWuEH34SMKvaO4wO_cHBw")
    subtitles = result["subtitles"]
    # 'none' language should be ignored
    assert "none" not in subtitles
    # English and Swedish subtitles should be present
    assert "en" in subtitles and subtitles["en"][0]["url"] == "http://captions.com/en.srt"
    assert "sv" in subtitles and subtitles["sv"][0]["url"] == "http://captions.com/sv.srt"
