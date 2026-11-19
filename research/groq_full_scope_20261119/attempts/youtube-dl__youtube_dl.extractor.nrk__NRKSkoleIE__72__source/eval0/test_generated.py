import pytest
from youtube_dl.extractor.nrk import NRKSkoleIE

@pytest.fixture
def ie():
    return NRKSkoleIE()

def test_real_extract_success(monkeypatch, ie):
    # Simulate a successful JSON response with a psId
    def fake_download_json(url, video_id):
        assert url == f'https://nrkno-skole-prod.kube.nrk.no/skole/api/media/{video_id}'
        assert video_id == '14099'
        return {'psId': '6021'}
    monkeypatch.setattr(ie, '_download_json', fake_download_json)

    result = ie._real_extract('https://www.nrk.no/skole/?page=search&q=&mediaId=14099')
    assert result.url == 'nrk:6021'
    assert result._type == 'url'

def test_real_extract_missing_psid(monkeypatch, ie):
    # Simulate JSON missing psId key
    def fake_download_json(url, video_id):
        return {}
    monkeypatch.setattr(ie, '_download_json', fake_download_json)

    with pytest.raises(KeyError):
        ie._real_extract('https://www.nrk.no/skole/?page=search&q=&mediaId=14099')

def test_real_extract_invalid_url(ie):
    # URL that does not match the pattern should raise ExtractorError
    with pytest.raises(ie.IEError):
        ie._real_extract('https://www.nrk.no/skole/?page=search&q=&mediaId=abc')
