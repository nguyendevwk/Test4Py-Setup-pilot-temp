import re
import json
import pytest
from youtube_dl.extractor.fourtube import FourTubeBaseIE
from youtube_dl.utils import ExtractorError

class DummyFourTubeIE(FourTubeBaseIE):
    _VALID_URL = r'https?://fourtube\.com/(?P<kind>m|v)/(?P<id>\d+)(?:/(?P<display_id>[^/]+))?'
    _URL_TEMPLATE = 'https://fourtube.com/v/%s'
    _TKN_HOST = 'example.com'

    def __init__(self, webpage, player_js=None, token_json=None):
        super().__init__(downloader=None)
        self._webpage = webpage
        self._player_js = player_js
        self._token_json = token_json

    def _download_webpage(self, url, video_id, note=None, errnote=None, headers=None, data=None, timeout=10, note_header=None):
        if 'playerembed' in url:
            return self._player_js
        return self._webpage

    def _download_json(self, url, video_id, data=None, headers=None, note=None, timeout=10):
        return self._token_json

    def _parse_json(self, s, video_id):
        return json.loads(s)

def test_extract_formats_with_media_id_and_sources(tmp_path):
    # Prepare dummy webpage containing media id and sources
    webpage = '''
    <html>
    <meta name="name" content="Test Video">
    <meta property="uploadDate" content="2023-01-01T12:00:00Z">
    <meta property="thumbnailUrl" content="https://example.com/thumb.jpg">
    <meta property="duration" content="PT2M30S">
    <button data-id="12345" data-quality="720p"></button>
    <button data-quality="480p"></button>
    </html>
    '''
    token_json = {"720p": "https://example.com/720p.mp4", "480p": "https://example.com/480p.mp4"}
    ie = DummyFourTubeIE(webpage, token_json=token_json)
    result = ie.extract('https://fourtube.com/v/98765')
    assert result['id'] == '98765'
    assert result['title'] == 'Test Video'
    assert result['thumbnail'] == 'https://example.com/thumb.jpg'
    assert result['duration'] == 150  # 2*60+30
    assert result['formats'][0]['url'] == 'https://example.com/720p.mp4'
    assert result['formats'][0]['format_id'] == '720p'
    assert result['formats'][0]['quality'] == 720
    assert len(result['formats']) == 2

def test_extract_formats_with_player_js_fallback(tmp_path):
    # Webpage missing media id, triggers player JS path
    webpage = '''
    <html>
    <meta name="name" content="Fallback Video">
    <meta property="uploadDate" content="2022-12-31T23:59:59Z">
    <meta property="thumbnailUrl" content="https://example.com/fallback.jpg">
    <meta property="duration" content="PT1M">
    <script id="playerembed" src="player.js"></script>
    </html>
    '''
    # Player JS contains ajax params: media id 55555 and qualities 360p,240p
    player_js = '''
    $.ajax(url, opts);
    });
    })([55555, null, [360, 240]]);
    '''
    token_json = {"360p": "https://example.com/360p.mp4", "240p": "https://example.com/240p.mp4"}
    ie = DummyFourTubeIE(webpage, player_js=player_js, token_json=token_json)
    result = ie.extract('https://fourtube.com/m/12345')
    assert result['id'] == '12345'
    assert result['title'] == 'Fallback Video'
    assert result['thumbnail'] == 'https://example.com/fallback.jpg'
    assert result['duration'] == 60
    # Formats should be sorted by quality descending
    assert result['formats'][0]['quality'] == 360
    assert result['formats'][1]['quality'] == 240
    assert len(result['formats']) == 2

def test_missing_title_raises_error(tmp_path):
    # Webpage without title meta
    webpage = '''
    <html>
    <meta property="uploadDate" content="2023-01-01T12:00:00Z">
    </html>
    '''
    ie = DummyFourTubeIE(webpage)
    with pytest.raises(ExtractorError):
        ie.extract('https://fourtube.com/v/99999')
