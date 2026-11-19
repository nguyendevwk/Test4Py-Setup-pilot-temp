import json
import re
import pytest
from youtube_dl.extractor.tvplay import ViafreeIE, TVPlayIE
from youtube_dl.utils import ExtractorError
from youtube_dl.compat import compat_HTTPError

# Helper to create a dummy extractor instance
@pytest.fixture
def extractor():
    return ViafreeIE()

# Test 1: suitable should return False when TVPlayIE is suitable
def test_suitable_precedence():
    url = "http://www.tvplay.no/some/path"
    # TVPlayIE.suitable returns True for this URL
    assert TVPlayIE.suitable(url) is True
    # ViafreeIE.suitable should defer to TVPlayIE and return False
    assert ViafreeIE.suitable(url) is False

# Test 2: successful extraction with mocked download_json
def test_real_extract_success(monkeypatch, extractor):
    # Mock content returned by the first download_json call
    mock_content = {
        "_embedded": {
            "viafreeBlocks": [
                {
                    "_embedded": {
                        "program": {
                            "guid": "12345",
                            "episode": {
                                "episodeNumber": "1",
                                "seasonNumber": "2",
                                "seriesTitle": "Test Series"
                            },
                            "video": {
                                "duration": {"milliseconds": 1116000}
                            },
                            "availability": {
                                "start": "2016-08-14T12:00:00Z"
                            },
                            "_links": {
                                "streamLink": {
                                    "href": "http://example.com/stream"
                                }
                            }
                        }
                    }
                }
            ]
        },
        "meta": {
            "title": "Test Title",
            "image": "http://example.com/thumbnail.jpg",
            "description": "Test description"
        }
    }

    # Mock stream JSON returned by the second download_json call
    mock_stream = {
        "embedded": {
            "prioritizedStreams": [
                {
                    "links": {
                        "stream": {
                            "href": "http://example.com/playlist.m3u8"
                        }
                    }
                }
            ]
        }
    }

    # Mock _download_json to return our dummy data
    def fake_download_json(url, video_id, *args, **kwargs):
        if "viafree-content" in url:
            return mock_content
        elif "example.com/stream" in url:
            return mock_stream
        raise ValueError(f"Unexpected URL: {url}")

    monkeypatch.setattr(extractor, "_download_json", fake_download_json)

    # Mock _extract_m3u8_formats to return a simple format list
    def fake_extract_m3u8_formats(url, video_id, ext):
        return [{"format_id": "720p", "url": url, "ext": ext}]
    monkeypatch.setattr(extractor, "_extract_m3u8_formats", fake_extract_m3u8_formats)

    # Mock _sort_formats to be a no-op
    monkeypatch.setattr(extractor, "_sort_formats", lambda x: None)

    # Run extraction
    result = extractor._real_extract("http://www.viafree.no/programmer/underholdning/det-beste-vorspielet/sesong-2/episode-1")

    # Assertions on the extracted data
    assert result["id"] == "12345"
    assert result["title"] == "Test Title"
    assert result["thumbnail"] == "http://example.com/thumbnail.jpg"
    assert result["description"] == "Test description"
    assert result["series"] == "Test Series"
    assert result["episode_number"] == 1
    assert result["season_number"] == 2
    assert result["duration"] == 1116
    assert result["timestamp"] == 1471200600
    assert result["formats"] == [{"format_id": "720p", "url": "http://example.com/playlist.m3u8", "ext": "mp4"}]

# Test 3: geo restriction handling
def test_geo_restricted(monkeypatch, extractor):
    # Mock content that triggers a 403 error on stream link
    mock_content = {
        "_embedded": {
            "viafreeBlocks": [
                {
                    "_embedded": {
                        "program": {
                            "guid": "12345",
                            "_links": {
                                "streamLink": {
                                    "href": "http://example.com/stream"
                                }
                            }
                        }
                    }
                }
            ]
        },
        "meta": {"title": "Test Title"}
    }

    def fake_download_json(url, video_id, *args, **kwargs):
        if "viafree-content" in url:
            return mock_content
        elif "example.com/stream" in url:
            raise ExtractorError("Forbidden", cause=compat_HTTPError(url, 403, "Forbidden", {}, ""))
        raise ValueError(f"Unexpected URL: {url}")

    monkeypatch.setattr(extractor, "_download_json", fake_download_json)

    # Expect a geo restriction error
    with pytest.raises(ExtractorError) as excinfo:
        extractor._real_extract("http://www.viafree.no/programmer/underholdning/det-beste-vorspielet/sesong-2/episode-1")
    assert "geo restricted" in str(excinfo.value).lower()
