import pytest
from youtube_dl.extractor.konserthusetplay import KonserthusetPlayIE
from youtube_dl.utils import determine_ext, int_or_none, float_or_none, url_or_none

class DummyKonserthusetPlayIE(KonserthusetPlayIE):
    """A subclass that overrides network calls to return controlled data."""
    def __init__(self, webpage, json_data):
        super().__init__()
        self._webpage = webpage
        self._json_data = json_data

    def _download_webpage(self, url, video_id, note=None, errnote=None, timeout=None, data=None, headers=None, query_string=None, referer=None, disposition=False, raw=False, errback=None, **kw):
        return self._webpage

    def _download_json(self, url, video_id, note=None, errnote=None, headers=None, data=None, query_string=None, timeout=None, errback=None, **kw):
        return self._json_data


def test_m3u8_format_extraction():
    """Test that an m3u8 URL is correctly extracted into formats."""
    webpage = 'http://example.com/?m=TESTID&e=abc'
    json_data = {
        'media': {
            'playerconfig': {
                'playlist': [
                    {
                        'url': 'http://stream.example.com/video_h264m.mp4',
                        'fallbackUrl': 'http://fallback.example.com/video_h264m.mp4',
                        'bitrates': [],
                        'captionsAvailableLanguages': {}
                    }
                ]
            },
            'title': 'Test Title',
            'image': 'http://example.com/thumb.jpg',
            'duration': 123456
        }
    }
    ie = DummyKonserthusetPlayIE(webpage, json_data)
    result = ie._real_extract('http://example.com/?m=TESTID')
    assert result['id'] == 'TESTID'
    assert result['title'] == 'Test Title'
    assert result['thumbnail'] == 'http://example.com/thumb.jpg'
    assert result['duration'] == 123.456
    # m3u8 extraction should produce at least one format
    assert any(f.get('ext') == 'mp4' for f in result['formats'])
    # fallback format should be present
    assert any(f.get('url') == 'http://fallback.example.com/video_h264m.mp4' for f in result['formats'])


def test_rtmp_and_fallback_format():
    """Test that RTMP formats are correctly constructed and fallback is added."""
    webpage = 'http://example.com/?m=RTMPID&e=xyz'
    json_data = {
        'media': {
            'playerconfig': {
                'rtmp': {'netConnectionUrl': 'rtmp://conn.example.com'},
                'playlist': [
                    {
                        'url': None,
                        'fallbackUrl': 'http://fallback.example.com/video_h264m.mp4',
                        'bitrates': [
                            {'url': 'http://stream.example.com/video_h264m.mp4', 'bitrate': 500000, 'width': 1280, 'height': 720},
                            {'url': 'http://stream.example.com/video_h264m_2.mp4', 'bitrate': 800000, 'width': 1920, 'height': 1080}
                        ],
                        'captionsAvailableLanguages': {}
                    }
                ]
            },
            'title': 'RTMP Title',
            'image': 'http://example.com/rtmp_thumb.jpg',
            'duration': 654321
        }
    }
    ie = DummyKonserthusetPlayIE(webpage, json_data)
    result = ie._real_extract('http://example.com/?m=RTMPID')
    # Check that RTMP formats are present
    rtmp_formats = [f for f in result['formats'] if f.get('url') == 'rtmp://conn.example.com']
    assert len(rtmp_formats) == 2
    # Check that fallback format is added for matching format id
    fallback_formats = [f for f in result['formats'] if f.get('url') == 'http://fallback.example.com/video_h264m.mp4']
    assert len(fallback_formats) == 1
    # Verify bitrate and dimensions
    for f in rtmp_formats:
        assert f['vbr'] in (500000, 800000)
        assert f['width'] in (1280, 1920)
        assert f['height'] in (720, 1080)


def test_subtitles_extraction():
    """Test that subtitles are extracted correctly from captionsAvailableLanguages."""
    webpage = 'http://example.com/?m=SUBID&e=def'
    json_data = {
        'media': {
            'playerconfig': {
                'playlist': [
                    {
                        'url': None,
                        'fallbackUrl': None,
                        'bitrates': [],
                        'captionsAvailableLanguages': {
                            'en': 'http://example.com/subs_en.vtt',
                            'sv': 'http://example.com/subs_sv.vtt',
                            'none': 'http://example.com/subs_none.vtt'
                        }
                    }
                ]
            },
            'title': 'Subtitle Title',
            'image': 'http://example.com/sub_thumb.jpg',
            'duration': 98765
        }
    }
    ie = DummyKonserthusetPlayIE(webpage, json_data)
    result = ie._real_extract('http://example.com/?m=SUBID')
    subtitles = result['subtitles']
    assert 'en' in subtitles
    assert 'sv' in subtitles
    assert 'none' not in subtitles
    assert subtitles['en'][0]['url'] == 'http://example.com/subs_en.vtt'
    assert subtitles['sv'][0]['url'] == 'http://example.com/subs_sv.vtt'
