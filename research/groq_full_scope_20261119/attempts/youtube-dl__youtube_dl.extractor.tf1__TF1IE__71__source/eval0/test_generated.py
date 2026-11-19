import json
import re
import pytest
from youtube_dl.extractor.tf1 import TF1IE

@pytest.fixture
def extractor():
    return TF1IE()

def mock_download_json(url, slug, query=None):
    # Return a minimal JSON structure that mimics the real API response
    return {
        'data': {
            'videoBySlug': {
                'streamId': 'wat123',
                'title': 'Test Video',
                'date': '2023-01-01T12:00:00Z',
                'publicPlayingInfos': {'duration': 3600},
                'tags': [{'label': 'tag1'}, {'label': ''}, {'label': 'tag2'}],
                'decoration': {
                    'image': {
                        'sources': [
                            {'url': 'https://example.com/thumb1.jpg', 'width': '640'},
                            {'url': None, 'width': '320'},
                            {'url': 'https://example.com/thumb2.jpg', 'width': None}
                        ]
                    },
                    'description': 'A description',
                    'programLabel': 'Test Series'
                },
                'season': '2',
                'episode': '5',
                'programSlug': 'test-program'
            }
        }
    }

def test_normal_extraction(extractor, monkeypatch):
    monkeypatch.setattr(extractor, "_download_json", mock_download_json)
    url = "https://www.tf1.fr/tmc/test-program/videos/test-video.html"
    result = extractor._real_extract(url)
    assert result['_type'] == 'url_transparent'
    assert result['id'] == 'wat123'
    assert result['url'] == 'wat:wat123'
    assert result['title'] == 'Test Video'
    assert result['description'] == 'A description'
    assert result['timestamp'] == 1672574400  # 2023-01-01T12:00:00Z
    assert result['duration'] == 3600
    assert result['tags'] == ['tag1', 'tag2']
    assert result['series'] == 'Test Series'
    assert result['season_number'] == 2
    assert result['episode_number'] == 5
    assert result['thumbnails'] == [
        {'url': 'https://example.com/thumb1.jpg', 'width': 640},
        {'url': 'https://example.com/thumb2.jpg', 'width': None}
    ]

def test_missing_tags_and_thumbnails(extractor, monkeypatch):
    def mock_no_tags(url, slug, query=None):
        return {
            'data': {
                'videoBySlug': {
                    'streamId': 'wat456',
                    'title': 'No Tags Video',
                    'date': '2023-02-02T00:00:00Z',
                    'publicPlayingInfos': {'duration': 120},
                    'tags': None,
                    'decoration': {
                        'image': {'sources': None},
                        'description': None,
                        'programLabel': None
                    },
                    'season': None,
                    'episode': None,
                    'programSlug': 'no-tags'
                }
            }
        }
    monkeypatch.setattr(extractor, "_download_json", mock_no_tags)
    url = "https://www.tf1.fr/tmc/no-tags/videos/no-tags-video.html"
    result = extractor._real_extract(url)
    assert result['tags'] == []
    assert result['thumbnails'] == []
    assert result['description'] is None
    assert result['series'] is None
    assert result['season_number'] is None
    assert result['episode_number'] is None

def test_invalid_url_raises(extractor):
    # URL that does not match the pattern should raise a ValueError
    with pytest.raises(ValueError):
        extractor._real_extract("https://www.example.com/not-a-tf1-url")
