import pytest
from youtube_dl.extractor.nrk import NRKSkoleIE

class DummyDownloader:
    def __init__(self, json_data):
        self.json_data = json_data
    def download(self, url, video_id):
        return self.json_data

def test_normal_extraction(monkeypatch):
    # Arrange: monkeypatch _download_json to return a known psId
    dummy_json = {'psId': '12345'}
    monkeypatch.setattr(NRKSkoleIE, "_download_json", lambda self, url, video_id: dummy_json)
    ie = NRKSkoleIE()
    # Act: extract
    result = ie.extract('https://www.nrk.no/skole/?page=search&q=&mediaId=14099')
    # Assert: result is a URLResult with correct format
    assert result.url == 'nrk:12345'
    assert result._type == 'url'
    assert result._ie_key == 'NRK'

def test_only_matching_url(monkeypatch):
    # Arrange: monkeypatch _download_json to raise if called
    monkeypatch.setattr(NRKSkoleIE, "_download_json", lambda self, url, video_id: (_ for _ in ()).throw(RuntimeError("Should not be called")))
    ie = NRKSkoleIE()
    # Act & Assert: extraction should raise ExtractorError because psId missing
    with pytest.raises(ie.IEError):
        ie.extract('https://www.nrk.no/skole/?page=objectives&subject=naturfag&objective=K15114&mediaId=19355')

def test_missing_psid_raises(monkeypatch):
    # Arrange: return JSON without psId
    dummy_json = {}
    monkeypatch.setattr(NRKSkoleIE, "_download_json", lambda self, url, video_id: dummy_json)
    ie = NRKSkoleIE()
    # Act & Assert: extraction should raise ExtractorError due to missing psId
    with pytest.raises(ie.IEError):
        ie.extract('https://www.nrk.no/skole/?page=search&q=&mediaId=14099')
