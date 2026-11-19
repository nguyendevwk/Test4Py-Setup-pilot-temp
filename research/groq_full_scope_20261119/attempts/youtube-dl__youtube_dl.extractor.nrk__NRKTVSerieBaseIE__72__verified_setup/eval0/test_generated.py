import pytest
from youtube_dl.extractor.nrk import NRKTVSerieBaseIE, NRKIE
from youtube_dl.utils import ExtractorError

# Helper to create a minimal instance of NRKTVSerieBaseIE
class DummyNRKIE(NRKTVSerieBaseIE):
    def __init__(self):
        # The base class expects a downloader; we pass None for simplicity
        super().__init__(downloader=None)

    # Override _call_api to avoid network calls during tests
    def _call_api(self, url, display_id, note=None, fatal=True):
        # Return None to simulate no further pages
        return None

def test_extract_entries_normal_and_boundary():
    ie = DummyNRKIE()
    # Normal case: list of dicts with valid prfId strings
    entries = ie._extract_entries([
        {'prfId': '123', 'episodeId': 'ignored'},
        {'episodeId': '456', 'prfId': None},
        {'prfId': '789'},
        {'prfId': 123},  # invalid type
        {'other': 'no id'},
    ])
    # Should produce three url_results with correct video_id
    assert len(entries) == 3
    for entry, vid in zip(entries, ['123', '789', '456']):
        assert entry['url'] == f'nrk:{vid}'
        assert entry['ie_key'] == NRKIE.ie_key()
        assert entry['video_id'] == vid

def test_extract_assets_key_and_catalog_name():
    ie = DummyNRKIE()
    # _extract_assets_key should return first matching key
    assert ie._extract_assets_key({'episodes': [], 'instalments': []}) == 'episodes'
    assert ie._extract_assets_key({'instalments': []}) == 'instalments'
    assert ie._extract_assets_key({'other': []}) is None

    # _catalog_name maps kinds correctly
    assert ie._catalog_name('podcast') == 'podcast'
    assert ie._catalog_name('podkast') == 'podcast'
    assert ie._catalog_name('series') == 'series'
    assert ie._catalog_name('unknown') == 'series'

def test_entries_pagination_and_termination():
    ie = DummyNRKIE()
    # Construct data with two pages of assets
    page1 = {
        '_embedded': {
            'episodes': {
                '_embedded': {
                    'episodes': [
                        {'prfId': 'a1'},
                        {'prfId': 'a2'},
                    ]
                },
                '_links': {
                    'next': {'href': 'next_page'}
                }
            }
        }
    }
    # The overridden _call_api will return None, so pagination stops after first page
    entries = list(ie._entries(page1, display_id='test'))
    # Should yield two entries from the first page only
    assert len(entries) == 2
    assert entries[0]['video_id'] == 'a1'
    assert entries[1]['video_id'] == 'a2'
