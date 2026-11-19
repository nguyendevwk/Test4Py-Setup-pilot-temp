import pytest
from youtube_dl.extractor.eitb import EitbIE
from youtube_dl.utils import sanitized_Request

class DummyIE(EitbIE):
    """Subclass to expose protected methods for testing."""
    pass

def test_extract_with_renditions(monkeypatch):
    # Prepare dummy JSON response
    video_id = '123456'
    dummy_video = {
        'web_media': [{
            'RENDITIONS': [
                {'PMD_URL': 'http://example.com/low.mp4', 'ENCODING_RATE': '500', 'FRAME_WIDTH': '640', 'FRAME_HEIGHT': '360'},
                {'PMD_URL': 'http://example.com/high.mp4', 'ENCODING_RATE': '1500', 'FRAME_WIDTH': '1280', 'FRAME_HEIGHT': '720'},
                {'PMD_URL': None, 'ENCODING_RATE': '2000'}  # should be skipped
            ],
            'NAME_ES': 'Test Video',
            'SHORT_DESC_ES': 'A test description',
            'STILL_URL': 'http://example.com/thumb.jpg',
            'LENGTH': '3000',
            'BROADCST_DATE': '2023-01-01 12:00:00',
            'TAGS': ['test', 'video']
        }]
    }

    # Mock methods
    monkeypatch.setattr(DummyIE, '_download_json', lambda self, url, video_id, *args, **kwargs: dummy_video)
    monkeypatch.setattr(DummyIE, '_extract_m3u8_formats', lambda self, url, video_id, *args, **kwargs: [])
    monkeypatch.setattr(DummyIE, '_extract_f4m_formats', lambda self, url, video_id, *args, **kwargs: [])
    monkeypatch.setattr(DummyIE, '_sort_formats', lambda self, formats: None)

    ie = DummyIE()
    result = ie._real_extract(f'http://www.eitb.tv/es/video/test/{video_id}')

    # Assertions
    assert result['id'] == video_id
    assert result['title'] == 'Test Video'
    assert result['description'] == 'A test description'
    assert result['thumbnail'] == 'http://example.com/thumb.jpg'
    assert result['duration'] == 3.0  # 3000 ms -> 3.0 seconds
    assert result['timestamp'] == 1672574400  # 2023-01-01 12:00:00 UTC
    assert result['tags'] == ['test', 'video']
    assert len(result['formats']) == 2
    urls = {f['url'] for f in result['formats']}
    assert 'http://example.com/low.mp4' in urls
    assert 'http://example.com/high.mp4' in urls

def test_extract_with_hls_token(monkeypatch):
    video_id = '654321'
    dummy_video = {
        'web_media': [{
            'RENDITIONS': [],
            'HLS_SURL': 'http://example.com/playlist.m3u8',
            'NAME_ES': 'HLS Video',
            'SHORT_DESC_ES': 'HLS test',
            'STILL_URL': None,
            'LENGTH': '6000',
            'BROADCST_DATE': '2023-02-02 10:00:00',
            'TAGS': []
        }]
    }
    dummy_token = {'token': 'abc123'}

    monkeypatch.setattr(DummyIE, '_download_json', lambda self, url, video_id, *args, **kwargs: dummy_video if 'ServiceMultiweb' in url else dummy_token)
    monkeypatch.setattr(DummyIE, '_extract_m3u8_formats', lambda self, url, video_id, *args, **kwargs: [{'url': url, 'format_id': 'hls'}])
    monkeypatch.setattr(DummyIE, '_extract_f4m_formats', lambda self, url, video_id, *args, **kwargs: [])
    monkeypatch.setattr(DummyIE, '_sort_formats', lambda self, formats: None)

    ie = DummyIE()
    result = ie._real_extract(f'http://www.eitb.tv/es/video/hls/{video_id}')

    assert result['id'] == video_id
    assert result['title'] == 'HLS Video'
    assert result['description'] == 'HLS test'
    assert result['thumbnail'] is None
    assert result['duration'] == 6.0
    assert result['timestamp'] == 1675356000  # 2023-02-02 10:00:00 UTC
    assert len(result['formats']) == 1
    assert result['formats'][0]['url'] == 'http://example.com/playlist.m3u8?hdnts=abc123'
    assert result['formats'][0]['format_id'] == 'hls'

def test_extract_with_hds(monkeypatch):
    video_id = '987654'
    dummy_video = {
        'web_media': [{
            'RENDITIONS': [],
            'HDS_SURL': 'http://example.com/stream.euskalsvod',
            'NAME_ES': 'HDS Video',
            'SHORT_DESC_ES': 'HDS test',
            'STILL_URL': None,
            'LENGTH': '12000',
            'BROADCST_DATE': '2023-03-03 08:30:00',
            'TAGS': []
        }]
    }

    monkeypatch.setattr(DummyIE, '_download_json', lambda self, url, video_id, *args, **kwargs: dummy_video)
    monkeypatch.setattr(DummyIE, '_extract_m3u8_formats', lambda self, url, video_id, *args, **kwargs: [])
    monkeypatch.setattr(DummyIE, '_extract_f4m_formats', lambda self, url, video_id, *args, **kwargs: [{'url': url, 'format_id': 'hds'}])
    monkeypatch.setattr(DummyIE, '_sort_formats', lambda self, formats: None)

    ie = DummyIE()
    result = ie._real_extract(f'http://www.eitb.tv/es/video/hds/{video_id}')

    assert result['id'] == video_id
    assert result['title'] == 'HDS Video'
    assert result['description'] == 'HDS test'
    assert result['thumbnail'] is None
    assert result['duration'] == 12.0
    assert result['timestamp'] == 1677879000  # 2023-03-03 08:30:00 UTC
    assert len(result['formats']) == 1
    assert result['formats'][0]['url'] == 'http://example.com/stream.euskalvod?hdcore=3.7.0'
    assert result['formats'][0]['format_id'] == 'hds'
