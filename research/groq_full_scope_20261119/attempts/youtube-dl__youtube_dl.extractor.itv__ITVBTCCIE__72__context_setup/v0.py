import pytest
from youtube_dl.extractor.itv import ITVBTCCIE
from youtube_dl.utils import ExtractorError

# Helper to create a fake webpage with given video IDs
def fake_webpage(video_ids):
    return ''.join(
        f'<div data-video-id="{vid}"></div>' for vid in video_ids
    )

def test_itvbtccie_normal_extraction(monkeypatch):
    """Test that a normal URL returns the expected playlist entries."""
    # Arrange
    url = 'http://www.itv.com/btcc/races/btcc-2018-all-the-action-from-brands-hatch'
    ie = ITVBTCCIE()
    # Mock the webpage download to return a page with three video IDs
    monkeypatch.setattr(
        ie, '_download_webpage',
        lambda u, i: fake_webpage(['123', '456', '789'])
    )
    # Act
    result = ie._real_extract(url)
    # Assert
    assert result['entries'] == [
        ie.url_result(
            'http://players.brightcove.net/1582188683001/HkiHLnNRx_default/index.html?videoId=123',
            ie=ie.ie_key(),
            video_id='123'
        ),
        ie.url_result(
            'http://players.brightcove.net/1582188683001/HkiHLnNRx_default/index.html?videoId=456',
            ie=ie.ie_key(),
            video_id='456'
        ),
        ie.url_result(
            'http://players.brightcove.net/1582188683001/HkiHLnNRx_default/index.html?videoId=789',
            ie=ie.ie_key(),
            video_id='789'
        ),
    ]
    assert result['id'] == 'btcc-2018-all-the-action-from-brands-hatch'
    assert result['title'] == 'BTCC 2018: All the action from Brands Hatch'

def test_itvbtccie_no_video_ids(monkeypatch):
    """Test that a page with no video IDs yields an empty playlist."""
    url = 'http://www.itv.com/btcc/races/empty'
    ie = ITVBTCCIE()
    monkeypatch.setattr(
        ie, '_download_webpage',
        lambda u, i: '<html><body>No videos here</body></html>'
    )
    result = ie._real_extract(url)
    assert result['entries'] == []
    assert result['id'] == 'empty'
    # Title may be None if not found
    assert result['title'] is None

def test_itvbtccie_invalid_url_raises():
    """Test that an invalid URL raises ExtractorError."""
    ie = ITVBTCCIE()
    with pytest.raises(ExtractorError):
        ie._real_extract('http://example.com/not-itv')
