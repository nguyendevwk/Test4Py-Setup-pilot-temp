import pytest
from youtube_dl.extractor.nrk import NRKBaseIE
from youtube_dl.utils import ExtractorError

class DummyIE(NRKBaseIE):
    IE_NAME = 'dummy'

def test_raise_error_geo_blocked_by_message_type():
    dummy = DummyIE()
    data = {'messageType': 'ProgramIsGeoBlocked'}
    with pytest.raises(ExtractorError) as excinfo:
        dummy._raise_error(data)
    assert 'NRK har ikke rettigheter' in str(excinfo.value)
    assert dummy._GEO_COUNTRIES == ['NO']

def test_raise_error_geo_blocked_by_usage_rights():
    dummy = DummyIE()
    data = {'usageRights': {'isGeoBlocked': True}}
    with pytest.raises(ExtractorError) as excinfo:
        dummy._raise_error(data)
    assert 'NRK har ikke rettigheter' in str(excinfo.value)
    assert dummy._GEO_COUNTRIES == ['NO']

def test_raise_error_other_message_type():
    dummy = DummyIE()
    data = {'messageType': 'ProgramRightsHasExpired', 'endUserMessage': 'Expired'}
    with pytest.raises(ExtractorError) as excinfo:
        dummy._raise_error(data)
    assert 'Expired' in str(excinfo.value)
    assert 'dummy said' in str(excinfo.value)
