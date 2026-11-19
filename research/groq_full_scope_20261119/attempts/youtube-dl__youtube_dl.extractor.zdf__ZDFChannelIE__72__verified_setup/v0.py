import pytest
from youtube_dl.extractor.zdf import ZDFChannelIE, ZDFIE
from youtube_dl.utils import InfoExtractor

# Helper to create a minimal InfoExtractor subclass that records calls
class DummyIE(InfoExtractor):
    def __init__(self):
        super().__init__()
        self.downloaded = []

    def _download_webpage(self, url, video_id, note=None, errnote=None, headers=None, data=None, timeout=None, note_on_error=None, errnote_on_error=None, fatal=True, add_dlc=False):
        self.downloaded.append((url, video_id))
        return self._webpage

    def _real_extract(self, url):
        return super()._real_extract(url)

@pytest.fixture
def dummy_ie():
    return DummyIE()

def test_real_extract_parses_plusbar_urls(dummy_ie):
    # Prepare a fake webpage containing two data-plusbar-url entries
    dummy_ie._webpage = '''
        <html>
            <body>
                <div data-plusbar-url="https://www.zdf.de/video1.html"></div>
                <div data-plusbar-url="https://www.zdf.de/video2.html"></div>
                <div data-plusbar-url="https://www.zdf.de/video1.html"></div> <!-- duplicate -->
            </body>
        </html>
    '''
    # Patch the IE key to avoid dependency on the real ZDFIE implementation
    dummy_ie.ie_key = lambda: 'ZDFIE'
    result = dummy_ie._real_extract('https://www.zdf.de/sport/das-aktuelle-sportstudio')
    # The playlist should contain two unique entries
    assert result['entries'] == [
        {'url': 'https://www.zdf.de/video1.html', 'ie': 'ZDFIE'},
        {'url': 'https://www.zdf.de/video2.html', 'ie': 'ZDFIE'}
    ]
    # The title should be extracted from og:title if present, otherwise None
    assert result['title'] is None

def test_real_extract_no_plusbar_urls(dummy_ie):
    # Webpage with no data-plusbar-url attributes
    dummy_ie._webpage = '<html><body>No videos here</body></html>'
    dummy_ie.ie_key = lambda: 'ZDFIE'
    result = dummy_ie._real_extract('https://www.zdf.de/filme/taunuskrimi/')
    # No entries should be returned
    assert result['entries'] == []
    # Title extraction should not raise an error
    assert result['title'] is None

def test_real_extract_invalid_url(dummy_ie):
    # The suitable method should return False for a URL that matches ZDFIE
    # We simulate this by monkeypatching ZDFIE.suitable to return True
    original_suitable = ZDFIE.suitable
    ZDFIE.suitable = staticmethod(lambda url: True)
    try:
        # Since ZDFChannelIE.suitable will delegate to ZDFIE.suitable and return False,
        # calling _real_extract should still work but we test that suitable logic is respected
        assert not ZDFChannelIE.suitable('https://www.zdf.de/sport/das-aktuelle-sportstudio')
    finally:
        ZDFIE.suitable = original_suitable
