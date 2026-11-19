import pytest
from youtube_dl.extractor.eitb import EitbIE
from youtube_dl.utils import sanitized_Request

class DummyDownloader:
    """A minimal downloader that records calls and returns preset data."""
    def __init__(self, json_data, token_data=None):
        self.json_data = json_data
        self.token_data = token_data
        self.downloaded_urls = []

    def _download_json(self, url, video_id, note=None, fatal=True):
        self.downloaded_urls.append(url)
        if 'TokenAuth' in url:
            return self.token_data
        return self.json_data

    def _extract_m3u8_formats(self, url, video_id, m3u8_id=None, fatal=True):
        return [{'url': url, 'format_id': m3u8_id}]

    def _extract_f4m_formats(self, url, video_id, f4m_id=None, fatal=True):
        return [{'url': url, 'format_id': f4m_id}]

    def _sort_formats(self, formats):
        # No-op for test
        pass

def test_valid_url_matches_and_id_extraction():
    url = 'https://www.eitb.tv/es/video/abc/123/456/7890/'
    ie = EitbIE()
    assert ie._VALID_URL.startswith('https?://')
    video_id = ie._match_id(url)
    assert video_id == '7890'

def test_real_extract_parses_basic_video_info(tmp_path):
    # Minimal JSON structure required by _real_extract
    json_data = {
        'web_media': [{
            'RENDITIONS': [
                {'PMD_URL': 'http://example.com/video.mp4',
                 'ENCODING_RATE': '1500',
                 'FRAME_WIDTH': '1280',
                 'FRAME_HEIGHT': '720'},
                {'PMD_URL': None}  # should be skipped
            ],
            'HLS_SURL': None,
            'HDS_SURL': None,
            'NAME_ES': 'Test Title',
            'SHORT_DESC_ES': 'Test Description',
            'STILL_URL': 'http://example.com/thumb.jpg',
            'LENGTH': '4000',
            'BROADCST_DATE': '2013-10-14 00:00:00',
            'TAGS': ['tag1', 'tag2']
        }],
        'desc_group': 'Group Description'
    }
    downloader = DummyDownloader(json_data)
    ie = EitbIE()
    ie._downloader = downloader
    result = ie._real_extract('http://www.eitb.tv/es/video/abc/123/456/7890/')
    assert result['id'] == '7890'
    assert result['title'] == 'Test Title'
    assert result['description'] == 'Test Description'
    assert result['thumbnail'] == 'http://example.com/thumb.jpg'
    assert result['duration'] == 4.0  # 4000 ms -> 4.0 seconds
    assert result['timestamp'] == 1381789200  # 2013-10-14 00:00:00 UTC
    assert result['tags'] == ['tag1', 'tag2']
    # formats should contain one valid rendition
    assert len(result['formats']) == 1
    fmt = result['formats'][0]
    assert fmt['url'] == 'http://example.com/video.mp4'
    assert fmt['format_id'] == 'http-1500'
    assert fmt['width'] == 1280
    assert fmt['height'] == 720
    assert fmt['tbr'] == 1500.0

def test_real_extract_ignores_missing_renditions_and_uses_token(tmp_path):
    # JSON with HLS_SURL and token data
    json_data = {
        'web_media': [{
            'RENDITIONS': [],
            'HLS_SURL': 'http://example.com/playlist.m3u8',
            'NAME_ES': 'HLS Title',
            'SHORT_DESC_ES': None,
            'STILL_URL': None,
            'LENGTH': '6000',
            'BROADCST_DATE': '2014-01-01 12:00:00',
            'TAGS': None
        }],
        'desc_group': None
    }
    token_data = {'token': 'abc123'}
    downloader = DummyDownloader(json_data, token_data)
    ie = EitbIE()
    ie._downloader = downloader
    result = ie._real_extract('http://www.eitb.tv/es/video/abc/123/456/7890/')
    # No renditions, but HLS should be added
    assert len(result['formats']) == 1
    fmt = result['formats'][0]
    assert fmt['url'] == 'http://example.com/playlist.m3u8?hdnts=abc123'
    assert fmt['format_id'] == 'hls'
    # Check other fields
    assert result['title'] == 'HLS Title'
    assert result['description'] == 'Group Description'
    assert result['duration'] == 6.0
    assert result['timestamp'] == 1388577600  # 2014-01-01 12:00:00 UTC
    assert result['tags'] is None
