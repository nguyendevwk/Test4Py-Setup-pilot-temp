import re
import pytest
from youtube_dl.extractor.trutv import TruTVIE

# Helper to create a fake downloader that returns predetermined JSON
class FakeDownloader:
    def __init__(self, json_data):
        self.json_data = json_data
    def _download_json(self, url, display_id):
        return self.json_data

def test_clip_extraction(monkeypatch):
    # Fake JSON response for a clip
    fake_json = {
        'info': {
            'mediaId': 'clip123',
            'title': '  Clip Title  ',
            'description': 'A short clip.',
            'images': [
                {'srcUrl': 'http://example.com/thumb1.jpg', 'width': '200', 'height': '100'},
                {'srcUrl': None, 'width': '100', 'height': '50'},  # should be skipped
            ],
            'publicationDate': '2023-01-01T12:00:00Z',
            'showTitle': 'Show Name',
            'seasonNum': '2',
            'episodeNum': '5',
        }
    }
    downloader = FakeDownloader(fake_json)
    ie = TruTVIE(downloader=downloader)
    url = 'https://www.trutv.com/shows/show-name/videos/clip-slug'
    info = ie._real_extract(url)

    assert info['id'] == 'clip123'
    assert info['display_id'] == 'clip-slug'
    assert info['title'] == 'Clip Title'
    assert info['description'] == 'A short clip.'
    assert info['series'] == 'Show Name'
    assert info['season_number'] == 2
    assert info['episode_number'] == 5
    assert len(info['thumbnails']) == 1
    thumb = info['thumbnails'][0]
    assert thumb['url'] == 'http://example.com/thumb1.jpg'
    assert thumb['width'] == 200
    assert thumb['height'] == 100

def test_episode_extraction(monkeypatch):
    # Fake JSON response for an episode
    fake_json = {
        'episode': {
            'mediaId': 'ep456',
            'title': 'Episode Title',
            'description': 'Full episode description.',
            'images': [],
            'publicationDate': '2022-12-31T23:59:59Z',
            'showTitle': 'Another Show',
            'seasonNum': None,
            'episodeNum': '10',
        }
    }
    downloader = FakeDownloader(fake_json)
    ie = TruTVIE(downloader=downloader)
    url = 'https://www.trutv.com/shows/another-show/12345'
    info = ie._real_extract(url)

    assert info['id'] == 'ep456'
    assert info['display_id'] == '12345'
    assert info['title'] == 'Episode Title'
    assert info['description'] == 'Full episode description.'
    assert info['series'] == 'Another Show'
    assert info['season_number'] is None
    assert info['episode_number'] == 10
    assert info['thumbnails'] == []

def test_invalid_url_raises(monkeypatch):
    ie = TruTVIE()
    # URL that does not match the regex should cause AttributeError when accessing groups
    bad_url = 'https://www.trutv.com/invalid/url'
    with pytest.raises(AttributeError):
        ie._real_extract(bad_url)
