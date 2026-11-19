import re
import pytest
from youtube_dl.extractor.trutv import TruTVIE
from youtube_dl.utils import parse_iso8601

class DummyDownloader:
    """A minimal downloader that records the last URL requested."""
    def __init__(self, data):
        self.data = data
        self.last_url = None

    def _download_json(self, url, display_id, *args, **kwargs):
        self.last_url = url
        return self.data

def test_episode_extract(tmp_path):
    # Prepare fake JSON response for an episode
    fake_json = {
        'episode': {
            'mediaId': '123abc',
            'title': '  Episode Title  ',
            'description': 'A description.',
            'images': [
                {'srcUrl': 'http://example.com/1.jpg', 'width': '640', 'height': '360'},
                {'srcUrl': None, 'width': '0', 'height': '0'},
            ],
            'publicationDate': '2023-01-01T12:00:00Z',
            'showTitle': 'Show Name',
            'seasonNum': '2',
            'episodeNum': '5',
            'isAuthRequired': False,
        }
    }
    downloader = DummyDownloader(fake_json)
    ie = TruTVIE(downloader)
    url = 'https://www.trutv.com/shows/show-slug/12345'
    info = ie._real_extract(url)

    assert info['id'] == '123abc'
    assert info['display_id'] == '12345'
    assert info['title'] == 'Episode Title'
    assert info['description'] == 'A description.'
    assert info['series'] == 'Show Name'
    assert info['season_number'] == 2
    assert info['episode_number'] == 5
    assert info['timestamp'] == parse_iso8601('2023-01-01T12:00:00Z')
    assert len(info['thumbnails']) == 1
    thumb = info['thumbnails'][0]
    assert thumb['url'] == 'http://example.com/1.jpg'
    assert thumb['width'] == 640
    assert thumb['height'] == 360
    # Verify that the correct API URL was requested
    assert downloader.last_url == 'https://api.trutv.com/v2/web/episode/show-slug/12345'

def test_clip_extract(tmp_path):
    # Prepare fake JSON response for a clip
    fake_json = {
        'info': {
            'mediaId': 'clip123',
            'title': 'Clip Title',
            'description': None,
            'images': [],
            'publicationDate': None,
            'showTitle': None,
            'seasonNum': None,
            'episodeNum': None,
            'isAuthRequired': True,
        }
    }
    downloader = DummyDownloader(fake_json)
    ie = TruTVIE(downloader)
    url = 'https://www.trutv.com/shows/show-slug/videos/clip-slug'
    info = ie._real_extract(url)

    assert info['id'] == 'clip123'
    assert info['display_id'] == 'clip-slug'
    assert info['title'] == 'Clip Title'
    assert info['description'] is None
    assert info['series'] is None
    assert info['season_number'] is None
    assert info['episode_number'] is None
    assert info['timestamp'] is None
    assert info['thumbnails'] == []
    assert info['auth_required'] is True
    # Verify that the correct API URL was requested
    assert downloader.last_url == 'https://api.trutv.com/v2/web/series/clip/show-slug/clip-slug'

def test_invalid_url_raises():
    ie = TruTVIE()
    with pytest.raises(AttributeError):
        # URL does not match the regex; re.match returns None leading to AttributeError
        ie._real_extract('https://www.trutv.com/invalid/url')
