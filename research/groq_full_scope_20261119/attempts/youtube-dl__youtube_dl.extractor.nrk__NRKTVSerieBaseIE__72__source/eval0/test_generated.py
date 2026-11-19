import pytest
from youtube_dl.extractor.nrk import NRKTVSerieBaseIE, NRKIE

class DummyNRKTVSerieBaseIE(NRKTVSerieBaseIE):
    def _call_api(self, *args, **kwargs):
        # Return None to stop pagination
        return None

def test_extract_entries_normal():
    ie = DummyNRKTVSerieBaseIE()
    entry_list = [
        {'prfId': '123', 'episodeId': 'ignored'},
        {'episodeId': '456', 'prfId': None},
        {'prfId': '789', 'episodeId': 'ignored'},
        {'prfId': None, 'episodeId': '000'},
        {'prfId': 123, 'episodeId': 'not_str'},
    ]
    entries = ie._extract_entries(entry_list)
    assert len(entries) == 3
    ids = [e['url'] for e in entries]
    assert ids == ['nrk:123', 'nrk:456', 'nrk:789']
    for e in entries:
        assert e['ie_key'] == NRKIE.ie_key()

def test_extract_assets_key_none():
    ie = DummyNRKTVSerieBaseIE()
    embedded = {'other_key': []}
    assert ie._extract_assets_key(embedded) is None

def test_entries_iteration():
    ie = DummyNRKTVSerieBaseIE()
    data = {
        '_embedded': {
            'episodes': {
                '_embedded': {
                    'episodes': [
                        {'prfId': 'a1'},
                        {'prfId': 'a2'},
                        {'prfId': None},
                    ]
                },
                '_links': {
                    'next': {'href': 'next_page'}
                }
            }
        }
    }
    entries = list(ie._entries(data, 'test_display_id'))
    assert len(entries) == 2
    assert entries[0]['url'] == 'nrk:a1'
    assert entries[1]['url'] == 'nrk:a2'
