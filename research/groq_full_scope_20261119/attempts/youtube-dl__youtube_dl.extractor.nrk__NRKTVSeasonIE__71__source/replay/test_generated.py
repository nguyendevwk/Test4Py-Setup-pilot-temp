import re
import pytest
from youtube_dl.extractor.nrk import NRKTVSeasonIE
from youtube_dl.utils import ExtractorError

class DummyNRKTVSeasonIE(NRKTVSeasonIE):
    def __init__(self, call_api_return, entries_return):
        super().__init__()
        self._call_api_return = call_api_return
        self._entries_return = entries_return

    def _call_api(self, url, display_id, name, query=None):
        return self._call_api_return

    def _entries(self, data, display_id):
        return self._entries_return

def test_numeric_season_id(monkeypatch):
    # Prepare dummy data for a numeric season id
    dummy_data = {
        'titles': {'title': 'Sesong 1'},
        'entries': [{'id': 'ep1'}, {'id': 'ep2'}]
    }
    dummy_entries = [{'id': 'ep1'}, {'id': 'ep2'}]
    extractor = DummyNRKTVSeasonIE(dummy_data, dummy_entries)

    result = extractor._real_extract('https://tv.nrk.no/serie/backstage/sesong/1')
    assert result['id'] == 'backstage/1'
    assert result['title'] == 'Sesong 1'
    assert result['entries'] == dummy_entries

def test_string_season_id(monkeypatch):
    # Prepare dummy data for a string season id
    dummy_data = {
        'titles': {'title': 'Diagnose kverulant'},
        'entries': [{'id': 'epA'}, {'id': 'epB'}]
    }
    dummy_entries = [{'id': 'epA'}, {'id': 'epB'}]
    extractor = DummyNRKTVSeasonIE(dummy_data, dummy_entries)

    result = extractor._real_extract('https://radio.nrk.no/podkast/hele_historien/sesong/diagnose-kverulant')
    assert result['id'] == 'hele_historien/diagnose-kverulant'
    assert result['title'] == 'Diagnose kverulant'
    assert result['entries'] == dummy_entries

def test_call_api_error(monkeypatch):
    # Simulate an API failure
    def raise_error(url, display_id, name, query=None):
        raise ExtractorError('API failure')
    extractor = DummyNRKTVSeasonIE(None, None)
    extractor._call_api = raise_error

    with pytest.raises(ExtractorError, match='API failure'):
        extractor._real_extract('https://tv.nrk.no/serie/backstage/sesong/1')
