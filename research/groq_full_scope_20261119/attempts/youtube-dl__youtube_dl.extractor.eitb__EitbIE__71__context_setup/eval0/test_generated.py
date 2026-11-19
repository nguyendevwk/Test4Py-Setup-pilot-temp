import json
import pytest
from youtube_dl.extractor.eitb import EitbIE

# Helper to create a minimal EitbIE instance with a dummy downloader
@pytest.fixture
def eitb_ie():
    return EitbIE()

def test_full_extraction(eitb_ie, tmp_path):
    # Prepare fake JSON responses
    video_id = '123456'
    video_json = {
        'web_media': [{
            'RENDITIONS': [
                {
                    'PMD_URL': 'http://example.com/video1.mp4',
                    'ENCODING_RATE': '1500',
                    'FRAME_WIDTH': '1280',
                    'FRAME_HEIGHT': '720'
                },
                {
                    'PMD_URL': 'http://example.com/video2.mp4',
                    'ENCODING_RATE': '800',
                    'FRAME_WIDTH': '640',
                    'FRAME_HEIGHT': '360'
                }
            ],
            'HLS_SURL': 'http://example.com/playlist.m3u8',
            'HDS_SURL': 'http://example.com/stream.f4m',
            'NAME_ES': 'Test Video',
            'SHORT_DESC_ES': 'A test description',
            'STILL_URL': 'http://example.com/thumb.jpg',
            'LENGTH': '120000',
            'BROADCST_DATE': '2023-01-01 12:00:00',
            'TAGS': ['tag1', 'tag2']
        }],
        'desc_group': 'Group description'
    }

    # Mock downloader methods
    def fake_download_json(url, video_id, *args, **kwargs):
        if 'ServiceMultiweb/Video' in url:
            return video_json
        if 'TokenAuth' in url:
            return {'token': 'abc123'}
        return {}

    def fake_extract_m3u8_formats(url, video_id, *args, **kwargs):
        return [{'url': url, 'format_id': 'hls'}]

    def fake_extract_f4m_formats(url, video_id, *args, **kwargs):
        return [{'url': url, 'format_id': 'hds'}]

    eitb_ie._download_json = fake_download_json
    eitb_ie._extract_m3u8_formats = fake_extract_m3u8_formats
    eitb_ie._extract_f4m_formats = fake_extract_f4m_formats

    # Run extraction
    result = eitb_ie._real_extract(f'http://www.eitb.tv/es/video/test/{video_id}')

    # Assertions
    assert result['id'] == video_id
    assert result['title'] == 'Test Video'
    assert result['description'] == 'A test description'
    assert result['thumbnail'] == 'http://example.com/thumb.jpg'
    assert result['duration'] == 120.0
    assert result['timestamp'] == 1672574400  # 2023-01-01 12:00:00 UTC
    assert result['tags'] == ['tag1', 'tag2']
    # Check formats
    formats = result['formats']
    assert any(f['url'] == 'http://example.com/video1.mp4' and f['tbr'] == 1500 for f in formats)
    assert any(f['url'] == 'http://example.com/video2.mp4' and f['tbr'] == 800 for f in formats)
    assert any(f['format_id'] == 'hls' for f in formats)
    assert any(f['format_id'] == 'hds' for f in formats)

def test_missing_renditions(eitb_ie):
    video_id = '654321'
    video_json = {
        'web_media': [{
            'RENDITIONS': [
                {'PMD_URL': None},
                {}
            ],
            'NAME_ES': 'No Renditions',
            'SHORT_DESC_ES': '',
            'STILL_URL': '',
            'LENGTH': None,
            'BROADCST_DATE': None,
            'TAGS': None
        }]
    }

    def fake_download_json(url, video_id, *args, **kwargs):
        return video_json

    eitb_ie._download_json = fake_download_json

    result = eitb_ie._real_extract(f'http://www.eitb.tv/es/video/test/{video_id}')

    assert result['id'] == video_id
    assert result['title'] == 'No Renditions'
    assert result['description'] == ''
    assert result['thumbnail'] == ''
    assert result['duration'] is None
    assert result['timestamp'] is None
    assert result['tags'] is None
    assert result['formats'] == []

def test_hls_token_missing(eitb_ie):
    video_id = '111222'
    video_json = {
        'web_media': [{
            'RENDITIONS': [],
            'HLS_SURL': 'http://example.com/playlist.m3u8',
            'NAME_ES': 'HLS Only',
            'SHORT_DESC_ES': 'Only HLS',
            'STILL_URL': '',
            'LENGTH': '60000',
            'BROADCST_DATE': '2022-12-31 23:59:59',
            'TAGS': []
        }]
    }

    def fake_download_json(url, video_id, *args, **kwargs):
        if 'ServiceMultiweb/Video' in url:
            return video_json
        if 'TokenAuth' in url:
            return {}  # No token
        return {}

    def fake_extract_m3u8_formats(url, video_id, *args, **kwargs):
        return [{'url': url, 'format_id': 'hls'}]

    eitb_ie._download_json = fake_download_json
    eitb_ie._extract_m3u8_formats = fake_extract_m3u8_formats

    result = eitb_ie._real_extract(f'http://www.eitb.tv/es/video/test/{video_id}')

    assert result['id'] == video_id
    assert result['title'] == 'HLS Only'
    assert result['description'] == 'Only HLS'
    assert result['duration'] == 60.0
    assert result['timestamp'] == 1672531199  # 2022-12-31 23:59:59 UTC
    assert result['tags'] == []
    # No formats because token missing
    assert result['formats'] == []
