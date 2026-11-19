import re
import pytest
from youtube_dl.extractor.zdf import ZDFChannelIE, ZDFIE

class DummyIE:
    @staticmethod
    def ie_key():
        return 'ZDFIE'

@pytest.fixture
def dummy_ie(monkeypatch):
    """Patch ZDFIE to a dummy implementation."""
    monkeypatch.setattr(ZDFIE, 'ie_key', staticmethod(DummyIE.ie_key))
    return DummyIE

def test_real_extract_parses_multiple_entries(monkeypatch, dummy_ie):
    """_real_extract should find all data-plusbar-url links and return them."""
    sample_html = '''
        <html>
            <body>
                <a data-plusbar-url="http://example.com/video1.html">Video 1</a>
                <a data-plusbar-url="http://example.com/video2.html">Video 2</a>
                <a data-plusbar-url="http://example.com/video1.html">Video 1 duplicate</a>
            </body>
        </html>
    '''
    # Patch the downloader methods
    monkeypatch.setattr(ZDFChannelIE, '_download_webpage', lambda self, url, channel_id: sample_html)
    monkeypatch.setattr(ZDFChannelIE, 'playlist_result', lambda self, entries, channel_id, title: {
        'entries': entries, 'id': channel_id, 'title': title
    })
    # Instantiate the extractor
    ie = ZDFChannelIE()
    result = ie._real_extract('https://www.zdf.de/sport/das-aktuelle-sportstudio')
    # There should be two unique entries
    assert len(result['entries']) == 2
    urls = {e['url'] for e in result['entries']}
    assert urls == {
        'http://example.com/video1.html',
        'http://example.com/video2.html',
    }
    # Each entry should specify the correct IE
    for e in result['entries']:
        assert e['ie'] == 'ZDFIE'

def test_real_extract_no_entries_returns_empty_playlist(monkeypatch, dummy_ie):
    """When no data-plusbar-url is present, playlist_result should still be called with empty entries."""
    sample_html = '<html><body>No video links here.</body></html>'
    monkeypatch.setattr(ZDFChannelIE, '_download_webpage', lambda self, url, channel_id: sample_html)
    monkeypatch.setattr(ZDFChannelIE, 'playlist_result', lambda self, entries, channel_id, title: {
        'entries': entries, 'id': channel_id, 'title': title
    })
    ie = ZDFChannelIE()
    result = ie._real_extract('https://www.zdf.de/filme/taunuskrimi/')
    assert result['entries'] == []
    assert result['id'] == 'taunuskrimi'
    assert result['title'] is None  # _og_search_title returns None if not found

def test_real_extract_uses_og_title_if_present(monkeypatch, dummy_ie):
    """_real_extract should use the og:title if available."""
    sample_html = '''
        <html>
            <head>
                <meta property="og:title" content="Test Channel Title">
            </head>
            <body>
                <a data-plusbar-url="http://example.com/video.html">Video</a>
            </body>
        </html>
    '''
    monkeypatch.setattr(ZDFChannelIE, '_download_webpage', lambda self, url, channel_id: sample_html)
    monkeypatch.setattr(ZDFChannelIE, 'playlist_result', lambda self, entries, channel_id, title: {
        'entries': entries, 'id': channel_id, 'title': title
    })
    ie = ZDFChannelIE()
    result = ie._real_extract('https://www.zdf.de/sport/das-aktuelle-sportstudio')
    assert result['title'] == 'Test Channel Title'
