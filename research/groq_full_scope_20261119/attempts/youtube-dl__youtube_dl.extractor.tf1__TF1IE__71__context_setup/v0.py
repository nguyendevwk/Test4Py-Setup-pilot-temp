import json
import re
import pytest
from youtube_dl.extractor.tf1 import TF1IE

# Helper to create a fake downloader that returns a controlled JSON
class FakeDownloader:
    def __init__(self, json_data):
        self.json_data = json_data

    def download_json(self, url, name, query=None):
        # ignore url and query, return the preset data
        return self.json_data

def test_tf1ie_normal_extraction(tmp_path):
    # Construct a URL that matches the regex
    url = 'https://www.tf1.fr/tmc/quotidien-avec-yann-barthes/videos/quotidien-premiere-partie-11-juin-2019.html'
    # Extract program_slug and slug from the URL
    match = re.match(TF1IE._VALID_URL, url)
    assert match is not None
    program_slug, slug = match.groups()

    # Prepare fake JSON response
    fake_json = {
        'data': {
            'videoBySlug': {
                'streamId': 'wat123',
                'title': 'Test Video',
                'date': '2019-06-11T12:00:00Z',
                'publicPlayingInfos': {'duration': 1234},
                'season': '2',
                'episode': '5',
                'tags': [{'label': 'tag1'}, {'label': 'tag2'}],
                'decoration': {
                    'image': {
                        'sources': [
                            {'url': 'http://thumb1.jpg', 'width': '640'},
                            {'url': 'http://thumb2.jpg', 'width': '1280'},
                        ]
                    },
                    'description': 'A description',
                    'programLabel': 'Series Name',
                },
            }
        }
    }

    # Monkeypatch the downloader
    tf1 = TF1IE()
    tf1._download_json = FakeDownloader(fake_json).download_json

    result = tf1._real_extract(url)

    assert result['_type'] == 'url_transparent'
    assert result['id'] == 'wat123'
    assert result['url'] == 'wat:wat123'
    assert result['title'] == 'Test Video'
    assert result['description'] == 'A description'
    assert result['timestamp'] == 1560273600  # 2019-06-11T12:00:00Z
    assert result['duration'] == 1234
    assert result['tags'] == ['tag1', 'tag2']
    assert result['series'] == 'Series Name'
    assert result['season_number'] == 2
    assert result['episode_number'] == 5
    assert result['thumbnails'] == [
        {'url': 'http://thumb1.jpg', 'width': 640},
        {'url': 'http://thumb2.jpg', 'width': 1280},
    ]

def test_tf1ie_missing_optional_fields(tmp_path):
    url = 'https://www.tf1.fr/tmc/quotidien-avec-yann-barthes/videos/quotidien-premiere-partie-11-juin-2019.html'
    match = re.match(TF1IE._VALID_URL, url)
    program_slug, slug = match.groups()

    # Fake JSON with missing tags, decoration, and width
    fake_json = {
        'data': {
            'videoBySlug': {
                'streamId': 'wat456',
                'title': 'No Tags',
                'date': '2020-01-01T00:00:00Z',
                'publicPlayingInfos': {'duration': None},
                'season': None,
                'episode': None,
                'tags': [],
                'decoration': {
                    'image': {
                        'sources': [
                            {'url': 'http://thumb3.jpg', 'width': None},
                            {'url': None, 'width': '800'},
                        ]
                    },
                    'description': None,
                    'programLabel': None,
                },
            }
        }
    }

    tf1 = TF1IE()
    tf1._download_json = FakeDownloader(fake_json).download_json

    result = tf1._real_extract(url)

    assert result['id'] == 'wat456'
    assert result['tags'] == []
    assert result['thumbnails'] == [{'url': 'http://thumb3.jpg', 'width': None}]
    assert result['description'] is None
    assert result['series'] is None
    assert result['season_number'] is None
    assert result['episode_number'] is None
    assert result['duration'] is None

def test_tf1ie_invalid_url_raises():
    tf1 = TF1IE()
    # URL that does not match the regex should raise a ValueError when re.match fails
    with pytest.raises(ValueError):
        tf1._real_extract('https://www.example.com/not-a-tf1-url')
