import json
import pytest
from youtube_dl.extractor.tf1 import TF1IE

# Helper to create a TF1IE instance with a mocked _download_json
def make_tf1ie(mock_response):
    ie = TF1IE()
    def mock_download_json(url, slug, query=None):
        # ignore arguments, return the mock response
        return mock_response
    ie._download_json = mock_download_json
    return ie

def test_normal_extraction(tmp_path):
    # Mock JSON response for a typical video
    mock_resp = {
        'data': {
            'videoBySlug': {
                'streamId': 'wat123',
                'title': 'Test Video',
                'date': '2023-01-01T12:00:00Z',
                'publicPlayingInfos': {'duration': 3600},
                'season': '2',
                'episode': '5',
                'tags': [{'label': 'tag1'}, {'label': 'tag2'}],
                'decoration': {
                    'description': 'A description',
                    'programLabel': 'Test Series',
                    'image': {
                        'sources': [
                            {'url': 'http://example.com/thumb1.jpg', 'width': '640'},
                            {'url': 'http://example.com/thumb2.jpg', 'width': None}
                        ]
                    }
                }
            }
        }
    }
    ie = make_tf1ie(mock_resp)
    result = ie._real_extract('https://www.tf1.fr/tmc/test-program/videos/test-video.html')
    assert result['_type'] == 'url_transparent'
    assert result['id'] == 'wat123'
    assert result['url'] == 'wat:wat123'
    assert result['title'] == 'Test Video'
    assert result['description'] == 'A description'
    assert result['series'] == 'Test Series'
    assert result['season_number'] == 2
    assert result['episode_number'] == 5
    assert result['duration'] == 3600
    assert result['tags'] == ['tag1', 'tag2']
    assert result['thumbnails'] == [
        {'url': 'http://example.com/thumb1.jpg', 'width': 640},
        {'url': 'http://example.com/thumb2.jpg', 'width': None}
    ]

def test_missing_tags_and_thumbnails(tmp_path):
    # Mock JSON response with missing tags and decoration image
    mock_resp = {
        'data': {
            'videoBySlug': {
                'streamId': 'wat456',
                'title': 'No Tags Video',
                'date': '2023-02-02T15:30:00Z',
                'publicPlayingInfos': {'duration': 1200},
                'season': None,
                'episode': None,
                'tags': [],
                'decoration': {
                    'description': 'No tags or thumbnails',
                    'programLabel': 'Series X',
                    'image': {
                        'sources': []
                    }
                }
            }
        }
    }
    ie = make_tf1ie(mock_resp)
    result = ie._real_extract('https://www.tf1.fr/tmc/no-tags/videos/no-tags-video.html')
    assert result['tags'] == []
    assert result['thumbnails'] == []
    assert result['season_number'] is None
    assert result['episode_number'] is None

def test_invalid_url_raises_value_error():
    ie = TF1IE()
    with pytest.raises(ValueError):
        ie._real_extract('https://www.invalid.com/not-a-tf1-url')
