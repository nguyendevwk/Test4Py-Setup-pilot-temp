import json
import re
import types
import pytest
from youtube_dl.extractor.zdf import ZDFBaseIE
from youtube_dl.utils import determine_ext, parse_codecs, qualities

class DummyZDFIE(ZDFBaseIE):
    """A minimal subclass that implements the abstract methods."""
    def __init__(self):
        super().__init__()
        self._download_json_calls = []

    def _download_json(self, url, video_id, note=None, headers=None):
        # Record the call for later inspection
        self._download_json_calls.append((url, video_id, note, headers))
        # Return a dummy JSON that will be overridden in tests
        return {}

    def _parse_json(self, json_str, video_id):
        return json.loads(json_str)

    def _search_regex(self, pattern, string, name, default=None, fatal=True, group=None):
        m = re.search(pattern, string)
        if not m:
            if fatal:
                raise ValueError(f"Regex {name} not found")
            return default
        return m.group(group) if group else m.group(0)

    def _extract_m3u8_formats(self, url, video_id, ext, **kwargs):
        return [{'url': url, 'format_id': 'hls', 'ext': ext}]

    def _extract_f4m_formats(self, url, video_id, **kwargs):
        return [{'url': url, 'format_id': 'hds', 'ext': 'f4m'}]

    def _sort_formats(self, formats):
        formats.sort(key=lambda f: f.get('quality', 0))

    @staticmethod
    def ie_key():
        return 'ZDF'

@pytest.fixture
def dummy():
    return DummyZDFIE()

def test_extract_subtitles_basic(dummy):
    src = {
        'captions': [
            {'uri': 'http://example.com/sub1.srt', 'language': 'eng'},
            {'uri': 'http://example.com/sub2.srt', 'language': 'deu'},
            {'uri': None, 'language': 'fre'},
            {'uri': 'http://example.com/sub3.srt'}  # default language
        ]
    }
    subtitles = dummy._extract_subtitles(src)
    assert 'eng' in subtitles
    assert 'deu' in subtitles
    assert 'fre' not in subtitles
    assert len(subtitles['eng']) == 1
    assert subtitles['eng'][0]['url'] == 'http://example.com/sub1.srt'
    assert subtitles['deu'][0]['url'] == 'http://example.com/sub2.srt'
    assert subtitles['deu'][0]['language'] == 'deu'
    # default language should be 'deu'
    assert subtitles['deu'][0]['url'] == 'http://example.com/sub3.srt'

def test_extract_format_m3u8_and_f4m(dummy):
    formats = []
    urls = set()
    # m3u8 case
    dummy._extract_format(
        video_id='vid1',
        formats=formats,
        format_urls=urls,
        meta={'url': 'http://example.com/stream.m3u8',
              'mimeType': 'application/x-mpegURL',
              'type': 'video',
              'quality': 'high',
              'mimeCodec': 'avc1.64001F',
              'language': 'eng'})
    assert any(f['format_id'] == 'hls' for f in formats)
    # f4m case
    dummy._extract_format(
        video_id='vid1',
        formats=formats,
        format_urls=urls,
        meta={'url': 'http://example.com/stream.f4m',
              'mimeType': 'application/f4m+xml',
              'type': 'video',
              'quality': 'low',
              'mimeCodec': 'avc1.42001E',
              'language': 'deu'})
    assert any(f['format_id'] == 'hds' for f in formats)
    # regular case
    dummy._extract_format(
        video_id='vid1',
        formats=formats,
        format_urls=urls,
        meta={'url': 'http://example.com/video.mp4',
              'mimeType': 'video/mp4',
              'type': 'video',
              'quality': 'med',
              'mimeCodec': 'avc1.4D401E',
              'language': 'fre'})
    # The format_id should include http, video, med
    assert any(f['format_id'] == 'http-video-med' for f in formats)
    # Ensure no duplicate URLs
    dummy._extract_format(
        video_id='vid1',
        formats=formats,
        format_urls=urls,
        meta={'url': 'http://example.com/video.mp4',
              'mimeType': 'video/mp4',
              'type': 'video',
              'quality': 'med',
              'mimeCodec': 'avc1.4D401E',
              'language': 'fre'})
    # formats length should not increase
    assert len(formats) == 3

def test_extract_ptmd_integration(dummy, monkeypatch):
    # Prepare a fake API response
    fake_ptmd = {
        'basename': 'test_video',
        'priorityList': [
            {
                'formitaeten': [
                    {
                        'qualities': [
                            {
                                'audio': {
                                    'tracks': [
                                        {'uri': 'http://example.com/audio1.mp3', 'language': 'eng'},
                                        {'uri': 'http://example.com/audio2.mp3', 'language': 'deu'}
                                    ]
                                },
                                'quality': 'low'
                            },
                            {
                                'audio': {
                                    'tracks': [
                                        {'uri': 'http://example.com/audio3.mp3', 'language': 'eng'}
                                    ]
                                },
                                'quality': 'high'
                            }
                        ],
                        'type': 'audio',
                        'mimeType': 'audio/mpeg',
                        'mimeCodec': 'mp3'
                    }
                ]
            }
        ],
        'attributes': {
            'duration': {'value': 120000}  # milliseconds
        },
        'captions': [
            {'uri': 'http://example.com/sub.srt', 'language': 'eng'}
        ]
    }

    def fake_download_json(url, video_id, note=None, headers=None):
        return fake_ptmd

    monkeypatch.setattr(dummy, '_download_json', fake_download_json)

    result = dummy._extract_ptmd(
        ptmd_url='http://api.example.com/ptmd',
        video_id='vid123',
        api_token='token',
        referrer='http://referrer.com'
    )

    assert result['extractor_key'] == 'ZDF'
    assert result['id'] == 'test_video'
    assert result['duration'] == 120.0  # seconds
    assert len(result['formats']) == 3
    # Check that formats have correct qualities
    qualities_map = {f['format_note']: f for f in result['formats']}
    assert 'low' in qualities_map
    assert 'high' in qualities_map
    # Subtitles extraction
    assert 'eng' in result['subtitles']
    assert result['subtitles']['eng'][0]['url'] == 'http://example.com/sub.srt'
