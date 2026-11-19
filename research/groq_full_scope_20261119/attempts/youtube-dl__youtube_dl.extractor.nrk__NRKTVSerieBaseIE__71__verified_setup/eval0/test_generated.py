import pytest
from youtube_dl.extractor.nrk import NRKTVSerieBaseIE, NRKIE
from youtube_dl.utils import ExtractorError

class DummyNRKTVSerieBaseIE(NRKTVSerieBaseIE):
    """A minimal subclass that does not perform real API calls."""
    def _call_api(self, url, display_id, note=None, fatal=True):
        # Return None to stop pagination
        return None

def test_extract_entries_valid_and_invalid():
    ie = DummyNRKTVSerieBaseIE()
    # Valid entries: mix of prfId and episodeId, both strings
    entry_list = [
        {'prfId': '12345', 'episodeId': 'ignored'},
        {'episodeId': '67890'},
        {'prfId': 123, 'episodeId': 'invalid_type'},  # invalid type
        {'prfId': None},  # missing id
    ]
    results = ie._extract_entries(entry_list)
    # Should return two results corresponding to the valid string ids
    assert len(results) == 2
    assert all(isinstance(r, dict) for r in results)
    # Check that the URLs are correctly formed
    assert results[0]['url'] == 'nrk:12345'
    assert results[1]['url'] == 'nrk:67890'
    # Ensure the IE key is NRKIE
    assert results[0]['ie'] == NRKIE.ie_key()

def test_extract_assets_key_returns_first_present():
    ie = DummyNRKTVSerieBaseIE()
    # Embedded dict with both keys; should return the first defined in _ASSETS_KEYS
    embedded = {'episodes': {'_embedded': {}}, 'instalments': {'_embedded': {}}}
    key = ie._extract_assets_key(embedded)
    assert key == 'episodes'
    # If only instalments present
    embedded = {'instalments': {'_embedded': {}}}
    key = ie._extract_assets_key(embedded)
    assert key == 'instalments'
    # If none present
    embedded = {'other': {}}
    key = ie._extract_assets_key(embedded)
    assert key is None

def test_catalog_name_boundary_cases():
    ie = DummyNRKTVSerieBaseIE()
    # Known podcast kinds
    assert ie._catalog_name('podcast') == 'podcast'
    assert ie._catalog_name('podkast') == 'podcast'
    # Any other kind defaults to series
    assert ie._catalog_name('drama') == 'series'
    assert ie._catalog_name('') == 'series'
    assert ie._catalog_name(None) == 'series'
