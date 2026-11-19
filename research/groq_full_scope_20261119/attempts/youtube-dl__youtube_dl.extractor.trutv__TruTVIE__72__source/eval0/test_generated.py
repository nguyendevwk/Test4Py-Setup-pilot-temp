import re
import pytest
from youtube_dl.extractor.trutv import TruTVIE

@pytest.fixture
def ie():
    return TruTVIE()

def test_episode_extract(monkeypatch, ie, tmp_path):
    # Prepare mock data for an episode
    mock_json = {
        'episode': {
            'mediaId': '12345',
            'title': '  Episode Title  ',
            'description': 'Desc',
            'images': [
                {'srcUrl': 'http://img1.jpg', 'width': '640', 'height': '360'},
                {'srcUrl': None, 'width': '320', 'height': '180'},
            ],
            'publicationDate': '2023-01-01T12:00:00Z',
            'showTitle': 'Show',
            'seasonNum': '2',
            'episodeNum': '5',
        }
    }
    # Mock _download_json to return mock_json
    def mock_download_json(url, display_id):
        assert url == 'https://api.trutv.com/v2/web/episode/the-carbonaro-effect/12345'
        assert display_id == '12345'
        return mock_json
    monkeypatch.setattr(ie, "_download_json", mock_download_json)

    # Mock _extract_ngtv_info to return a base dict
    def mock_extract_ngtv_info(media_id, _, meta):
        assert media_id == '12345'
        assert meta['url'] == 'https://www.trutv.com/shows/the-carbonaro-effect/videos/sunlight-activated-flower.html'
        assert meta['site_name'] == 'truTV'
        return {'dummy': 'value'}

    monkeypatch.setattr(ie, "_extract_ngtv_info", mock_extract_ngtv_info)

    url = 'https://www.trutv.com/shows/the-carbonaro-effect/videos/sunlight-activated-flower.html'
    info = ie._real_extract(url)

    assert info['id'] == '12345'
    assert info['display_id'] == '12345'
    assert info['title'] == 'Episode Title'
    assert info['description'] == 'Desc'
    assert info['series'] == 'Show'
    assert info['season_number'] == 2
    assert info['episode_number'] == 5
    assert info['thumbnails'] == [{'url': 'http://img1.jpg', 'width': 640, 'height': 360}]
    assert info['timestamp'] == 1672574400  # 2023-01-01T12:00:00Z in epoch

def test_series_clip_extract(monkeypatch, ie):
    # Prepare mock data for a series clip
    mock_json = {
        'info': {
            'mediaId': 'clip123',
            'title': 'Clip Title',
            'description': None,
            'images': [],
            'publicationDate': None,
            'showTitle': None,
            'seasonNum': None,
            'episodeNum': None,
        }
    }
    def mock_download_json(url, display_id):
        assert url == 'https://api.trutv.com/v2/web/series/clip/the-carbonaro-effect/sunlight-activated-flower'
        assert display_id == 'sunlight-activated-flower'
        return mock_json
    monkeypatch.setattr(ie, "_download_json", mock_download_json)

    def mock_extract_ngtv_info(media_id, _, meta):
        assert media_id == 'clip123'
        return {'dummy': 'value'}

    monkeypatch.setattr(ie, "_extract_ngtv_info", mock_extract_ngtv_info)

    url = 'https://www.trutv.com/shows/the-carbonaro-effect/videos/sunlight-activated-flower'
    info = ie._real_extract(url)

    assert info['id'] == 'clip123'
    assert info['display_id'] == 'sunlight-activated-flower'
    assert info['title'] == 'Clip Title'
    assert info['description'] is None
    assert info['thumbnails'] == []
    assert info['timestamp'] is None
    assert info['series'] is None
    assert info['season_number'] is None
    assert info['episode_number'] is None

def test_invalid_url_raises(monkeypatch, ie):
    # Ensure that an invalid URL raises a regex match error
    url = 'https://www.trutv.com/invalid/url'
    with pytest.raises(AttributeError):
        ie._real_extract(url)
