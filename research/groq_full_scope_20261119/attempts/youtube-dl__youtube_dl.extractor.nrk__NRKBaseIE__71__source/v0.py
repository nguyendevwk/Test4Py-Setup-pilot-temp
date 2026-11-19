import re
import pytest
from youtube_dl.extractor.nrk import NRKBaseIE
from youtube_dl.utils import ExtractorError

class DummyNRK(NRKBaseIE):
    def __init__(self):
        super().__init__()
        self._download_json_called = False

    def _download_json(self, url, video_id, note, fatal=True, query=None, headers=None):
        self._download_json_called = True
        return {}

def test_raise_error_geo_blocked(monkeypatch):
    dummy = DummyNRK()
    data = {'messageType': 'ProgramIsGeoBlocked'}
    with pytest.raises(ExtractorError) as excinfo:
        dummy._raise_error(data)
    assert 'NRK har ikke rettigheter' in str(excinfo.value)
    assert dummy._GEO_COUNTRIES == ['NO']

def test_raise_error_other_message(monkeypatch):
    dummy = DummyNRK()
    data = {'messageType': 'ProgramRightsHasExpired', 'endUserMessage': 'Expired'}
    with pytest.raises(ExtractorError) as excinfo:
        dummy._raise_error(data)
    assert 'Expired' in str(excinfo.value)
    assert 'ProgramRightsHasExpired' not in str(excinfo.value)

def test_extract_nrk_formats_akamai(monkeypatch):
    dummy = DummyNRK()
    asset_url = 'https://example.akamaihd.net/i/12345'
    video_id = 'vid123'
    # Mock the akamai extraction to return a known list
    def fake_akamai(url, vid):
        return [{'url': url, 'format_id': 'akamai'}]
    monkeypatch.setattr(dummy, '_extract_akamai_formats', fake_akamai)
    formats = dummy._extract_nrk_formats(asset_url, video_id)
    assert isinstance(formats, list)
    assert formats[0]['format_id'] == 'akamai'
    assert formats[0]['url'] == asset_url
