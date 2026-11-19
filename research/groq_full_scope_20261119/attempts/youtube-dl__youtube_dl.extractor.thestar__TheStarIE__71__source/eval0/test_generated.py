import pytest
from youtube_dl.extractor.thestar import TheStarIE
from youtube_dl.utils import ExtractorError

def test_suitable_url_matches():
    ie = TheStarIE()
    assert ie.suitable('https://www.thestar.com/some/path/12345.html')
    assert not ie.suitable('https://example.com/12345.html')

def test_real_extract_returns_brightcove_url(monkeypatch):
    ie = TheStarIE()
    # Mock _download_webpage to return a page containing the brightcove id
    def fake_download_webpage(url, display_id):
        return '... mainartBrightcoveVideoId: "123456789" ...'
    monkeypatch.setattr(ie, '_download_webpage', fake_download_webpage)
    result = ie._real_extract('https://www.thestar.com/some/path/12345.html')
    assert result.url == 'http://players.brightcove.net/794267642001/default_default/index.html?videoId=123456789'
    assert result.ie_key == 'BrightcoveNew'
    assert result.info_dict['id'] == '123456789'

def test_real_extract_missing_brightcove_id_raises(monkeypatch):
    ie = TheStarIE()
    # Mock _download_webpage to return a page without the brightcove id
    def fake_download_webpage(url, display_id):
        return '... no brightcove id here ...'
    monkeypatch.setattr(ie, '_download_webpage', fake_download_webpage)
    with pytest.raises(ExtractorError):
        ie._real_extract('https://www.thestar.com/some/path/12345.html')
