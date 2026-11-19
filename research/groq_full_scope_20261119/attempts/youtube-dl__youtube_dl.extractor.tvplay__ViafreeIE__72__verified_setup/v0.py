import json
import re
import types
import pytest
from youtube_dl.extractor.tvplay import ViafreeIE
from youtube_dl.utils import ExtractorError
from youtube_dl.compat import compat_HTTPError

# Helper to create a dummy downloader with minimal interface
class DummyDownloader:
    def __init__(self):
        self.last_url = None
        self.last_headers = None

    def _download_json(self, url, name, headers=None):
        self.last_url = url
        self.last_headers = headers
        return self._json_response

    def _extract_m3u8_formats(self, url, video_id, ext):
        return [{'url': url, 'format_id': '720p', 'ext': ext}]

    def _sort_formats(self, formats):
        pass

    def geo_verification_headers(self):
        return {'User-Agent': 'test'}

    def raise_geo_restricted(self, countries):
        raise ExtractorError('geo restricted', cause=compat_HTTPError(403, 'Forbidden'))

# Test normal extraction path
def test_viafree_normal_extraction(tmp_path):
    ie = ViafreeIE(DummyDownloader())
    # Prepare fake JSON responses
    ie._json_response = {
        "_embedded": {
            "viafreeBlocks": [
                {
                    "_embedded": {
                        "program": {
                            "guid": "12345",
                            "title": "Test Title",
                            "episode": {
                                "seriesTitle": "Test Series",
                                "episodeNumber": "7",
                                "seasonNumber": "2"
                            },
                            "video": {
                                "duration": {"milliseconds": 60000}
                            },
                            "availability": {"start": "2021-01-01T00:00:00Z"},
                            "_links": {
                                "streamLink": {
                                    "href": "https://stream.example.com/link"
                                }
                            }
                        }
                    }
                }
            ]
        },
        "meta": {
            "title": "Test Title",
            "image": "https://example.com/thumb.jpg",
            "description": "Test description"
        }
    }
    # Mock stream link JSON
    def mock_download_json(url, name, headers=None):
        if "stream.example.com" in url:
            return {
                "embedded": {
                    "prioritizedStreams": [
                        {
                            "links": {
                                "stream": {"href": "https://cdn.example.com/video.m3u8"}
                            }
                        }
                    ]
                }
            }
        return ie._json_response
    ie._download_json = mock_download_json

    result = ie.extract('http://www.viafree.no/programmer/underholdning/det-beste-vorspielet/sesong-2/episode-1')
    assert result['id'] == '12345'
    assert result['title'] == 'Test Title'
    assert result['series'] == 'Test Series'
    assert result['episode_number'] == 7
    assert result['season_number'] == 2
    assert result['duration'] == 60
    assert result['timestamp'] == 1609459200  # 2021-01-01T00:00:00Z
    assert result['thumbnail'] == 'https://example.com/thumb.jpg'
    assert result['description'] == 'Test description'
    assert result['formats'][0]['url'] == 'https://cdn.example.com/video.m3u8'

# Test geo restriction handling
def test_viafree_geo_restriction(tmp_path):
    ie = ViafreeIE(DummyDownloader())
    ie._json_response = {
        "_embedded": {
            "viafreeBlocks": [
                {
                    "_embedded": {
                        "program": {
                            "guid": "12345",
                            "title": "Test Title",
                            "episode": {},
                            "video": {"duration": {"milliseconds": 60000}},
                            "availability": {"start": "2021-01-01T00:00:00Z"},
                            "_links": {
                                "streamLink": {
                                    "href": "https://stream.example.com/link"
                                }
                            }
                        }
                    }
                }
            ]
        },
        "meta": {"title": "Test Title"}
    }
    def mock_download_json(url, name, headers=None):
        if "stream.example.com" in url:
            raise ExtractorError('geo', cause=compat_HTTPError(403, 'Forbidden'))
        return ie._json_response
    ie._download_json = mock_download_json
    with pytest.raises(ExtractorError) as excinfo:
        ie.extract('http://www.viafree.dk/programmer/reality/paradise-hotel/saeson-7/episode-5')
    assert 'geo restricted' in str(excinfo.value)

# Test missing optional fields
def test_viafree_missing_fields(tmp_path):
    ie = ViafreeIE(DummyDownloader())
    ie._json_response = {
        "_embedded": {
            "viafreeBlocks": [
                {
                    "_embedded": {
                        "program": {
                            "guid": "12345",
                            "title": "Test Title",
                            "episode": {},
                            "video": {"duration": {"milliseconds": 120000}},
                            "availability": {"start": "2021-01-01T00:00:00Z"},
                            "_links": {
                                "streamLink": {
                                    "href": "https://stream.example.com/link"
                                }
                            }
                        }
                    }
                }
            ]
        },
        "meta": {"title": "Test Title"}
    }
    def mock_download_json(url, name, headers=None):
        if "stream.example.com" in url:
            return {
                "embedded": {
                    "prioritizedStreams": [
                        {"links": {"stream": {"href": "https://cdn.example.com/video.m3u8"}}}
                    ]
                }
            }
        return ie._json_response
    ie._download_json = mock_download_json
    result = ie.extract('http://www.viafree.se/program/reality/sommaren-med-youtube-stjarnorna/sasong-1/avsnitt-1')
    assert result['series'] is None
    assert result['episode_number'] is None
    assert result['season_number'] is None
    assert result['duration'] == 120
    assert result['timestamp'] == 1609459200
