import re
import pytest
from youtube_dl.extractor.itv import ITVBTCCIE
from youtube_dl.extractor.brightcove import BrightcoveNewIE


class DummyITVIE(ITVBTCCIE):
    """Subclass that overrides webpage download for testing."""
    def __init__(self, webpage: str):
        super().__init__()
        self._webpage = webpage

    def _download_webpage(self, url, video_id, note=None, errnote=None, *, data=None, headers=None, query=None, timeout=None, fatal=True):
        # Return the pre‑provided webpage regardless of URL
        return self._webpage


def test_itvbtccie_multiple_videos(tmp_path):
    # Prepare a fake webpage containing three video IDs
    fake_webpage = '''
        <html>
            <div data-video-id="12345"></div>
            <div data-video-id="67890"></div>
            <div data-video-id="abcde"></div>
        </html>
    '''
    ie = DummyITVIE(fake_webpage)
    result = ie._real_extract('http://www.itv.com/btcc/test/playlist')
    # The result should be a playlist with three entries
    assert result['entries'] is not None
    assert len(result['entries']) == 3
    # Each entry should be a Brightcove URL smuggled with geo blocks and referrer
    for entry, vid in zip(result['entries'], ['12345', '67890', 'abcde']):
        assert entry['url'].startswith('http://players.brightcove.net/1582188683001/HkiHLnNRx_default/index.html?videoId=')
        assert f'videoId={vid}' in entry['url']
        # Check that smuggled parameters are present
        assert 'geo_ip_blocks' in entry['url']
        assert 'referrer' in entry['url']
    # Title should be None because _og_search_title fails on fake page
    assert result['title'] is None


def test_itvbtccie_no_videos(tmp_path):
    # Webpage with no data-video-id attributes
    fake_webpage = '<html><body>No videos here</body></html>'
    ie = DummyITVIE(fake_webpage)
    result = ie._real_extract('http://www.itv.com/btcc/empty')
    # No entries should be produced
    assert result['entries'] == []
    # Title remains None
    assert result['title'] is None


def test_itvbtccie_invalid_url():
    # URL that does not match the expected pattern should raise a ValueError
    with pytest.raises(ValueError):
        ITVBTCCIE()._real_extract('http://example.com/not-itv')
