import pytest
from youtube_dl.extractor.nrk import NRKBaseIE
from youtube_dl.utils import ExtractorError

# Create a minimal concrete subclass of NRKBaseIE for testing
class DummyNRKIE(NRKBaseIE):
    IE_NAME = 'dummy_nrk'
    _VALID_URL = r'https?://dummy\.com/.*'
    _TEST = {'url': 'https://dummy.com', 'info_dict': {'id': 'dummy', 'ext': 'mp4'}}

    def _real_extract(self, url):
        return {}

def test_raise_error_geo_blocked():
    ie = DummyNRKIE()
    data = {'messageType': 'ProgramIsGeoBlocked'}
    with pytest.raises(ExtractorError) as excinfo:
        ie._raise_error(data)
    assert 'NRK har ikke rettigheter' in str(excinfo.value)
    assert ie._GEO_COUNTRIES == ['NO']

def test_raise_error_usage_rights_geo_blocked():
    ie = DummyNRKIE()
    data = {'usageRights': {'isGeoBlocked': True}}
    with pytest.raises(ExtractorError) as excinfo:
        ie._raise_error(data)
    assert 'NRK har ikke rettigheter' in str(excinfo.value)

def test_raise_error_other_message():
    ie = DummyNRKIE()
    data = {'messageType': 'ProgramRightsHasExpired', 'endUserMessage': 'Expired'}
    with pytest.raises(ExtractorError) as excinfo:
        ie._raise_error(data)
    assert 'Expired' in str(excinfo.value)
    assert 'dummy_nrk' in str(excinfo.value)
