import json
import re
import pytest
from youtube_dl.extractor.tvplay import ViafreeIE, TVPlayIE
from youtube_dl.utils import ExtractorError
from youtube_dl.compat import compat_HTTPError


def test_suitable_excludes_tvplay():
    """ViafreeIE.suitable should return False for URLs that TVPlayIE considers suitable."""
    url = "http://www.viafree.no/programmer/underholdning/det-beste-vorspielet/sesong-2/episode-1"
    assert TVPlayIE.suitable(url) is True
    assert ViafreeIE.suitable(url) is False


def test_real_extract_success(monkeypatch, tmp_path):
    """_real_extract should parse JSON and return expected fields."""
    # Prepare dummy JSON responses
    content_json = {
        "_embedded": {
            "viafreeBlocks": [
                {
                    "_embedded": {
                        "program": {
                            "guid": "12345",
                            "episode": {
                                "seriesTitle": "Test Series",
                                "episodeNumber": "7",
                                "seasonNumber": "2"
                            },
                            "video": {
                                "duration": {"milliseconds": 123456}
                            },
                            "availability": {"start": "2023-01-01T12:00:00Z"}
                        }
                    }
                }
            ]
        },
        "meta": {
            "title": "Test Title",
            "image": "http://example.com/thumb.jpg",
            "description": "Test description"
        }
    }

    stream_json = {
        "embedded": {
            "prioritizedStreams": [
                {
                    "links": {
                        "stream": {"href": "http://example.com/stream.m3u8"}
                    }
                }
            ]
        }
    }

    # Mock download_json to return our dummy data
    def fake_download_json(url, name, *args, **kwargs):
        if "viafree-content" in url:
            return content_json
        if "streamLink" in url:
            return stream_json
        raise ValueError(f"Unexpected URL: {url}")

    monkeypatch.setattr(ViafreeIE, "_download_json", fake_download_json)

    # Mock _extract_m3u8_formats to return a simple format list
    def fake_extract_m3u8_formats(url, video_id, ext):
        return [{"format_id": "720p", "url": url, "ext": ext}]
    monkeypatch.setattr(ViafreeIE, "_extract_m3u8_formats", fake_extract_m3u8_formats)

    # Mock _sort_formats to do nothing
    monkeypatch.setattr(ViafreeIE, "_sort_formats", lambda self, formats: None)

    # Instantiate extractor and call _real_extract
    extractor = ViafreeIE()
    result = extractor._real_extract(
        "http://www.viafree.no/programmer/underholdning/det-beste-vorspielet/sesong-2/episode-1"
    )

    # Assertions on the returned dictionary
    assert result["id"] == "12345"
    assert result["title"] == "Test Title"
    assert result["thumbnail"] == "http://example.com/thumb.jpg"
    assert result["description"] == "Test description"
    assert result["series"] == "Test Series"
    assert result["episode_number"] == 7
    assert result["season_number"] == 2
    assert result["duration"] == 123
    assert result["timestamp"] == 1672574400  # 2023-01-01T12:00:00Z
    assert result["formats"] == [{"format_id": "720p", "url": "http://example.com/stream.m3u8", "ext": "mp4"}]


def test_geo_restricted(monkeypatch):
    """_real_extract should raise geo restriction when stream link returns 403."""
    # Dummy content JSON
    content_json = {
        "_embedded": {
            "viafreeBlocks": [
                {
                    "_embedded": {
                        "program": {
                            "guid": "12345",
                            "episode": {},
                            "video": {"duration": {"milliseconds": 0}},
                            "availability": {"start": None}
                        }
                    }
                }
            ]
        },
        "meta": {"title": "Test Title"}
    }

    def fake_download_json(url, name, *args, **kwargs):
        if "viafree-content" in url:
            return content_json
        if "streamLink" in url:
            raise ExtractorError(
                "Forbidden",
                cause=compat_HTTPError(url, 403, "Forbidden", {}, None)
            )
        raise ValueError(f"Unexpected URL: {url}")

    monkeypatch.setattr(ViafreeIE, "_download_json", fake_download_json)

    extractor = ViafreeIE()
    with pytest.raises(ExtractorError) as excinfo:
        extractor._real_extract(
            "http://www.viafree.no/programmer/underholdning/det-beste-vorspielet/sesong-2/episode-1"
        )
    assert "geo restricted" in str(excinfo.value).lower()
