import pytest
from youtube_dl.extractor.nrk import NRKTVSerieBaseIE, NRKIE


def test_extract_entries_valid_and_invalid():
    ie = NRKTVSerieBaseIE()
    # Valid list with proper IDs
    entries = ie._extract_entries([
        {'prfId': '123'},          # valid
        {'episodeId': 'abc'},      # valid
        {'prfId': 456},            # invalid type
        {'prfId': None},           # invalid value
        {},                         # no ID
    ])
    # Should return two url_results
    assert len(entries) == 2
    assert all(isinstance(e, type(ie.url_result('nrk:dummy', ie=NRKIE.ie_key(), video_id='dummy'))) for e in entries)
    assert entries[0].url == 'nrk:123'
    assert entries[1].url == 'nrk:abc'

    # Non-list input returns empty list
    assert ie._extract_entries('not a list') == []


def test_extract_assets_key_and_catalog_name():
    ie = NRKTVSerieBaseIE()
    # _extract_assets_key should return first matching key
    assert ie._extract_assets_key({'episodes': [], 'instalments': []}) == 'episodes'
    assert ie._extract_assets_key({'instalments': []}) == 'instalments'
    assert ie._extract_assets_key({'other': []}) is None

    # _catalog_name maps kinds correctly
    assert ie._catalog_name('podcast') == 'podcast'
    assert ie._catalog_name('podkast') == 'podcast'
    assert ie._catalog_name('series') == 'series'
    assert ie._catalog_name('unknown') == 'series'


def test_entries_pagination_and_next_url(monkeypatch):
    ie = NRKTVSerieBaseIE()
    # Prepare a sequence of two pages
    page1 = {
        '_embedded': {
            'episodes': {
                '_embedded': {
                    'episodes': [
                        {'prfId': '1'},
                        {'prfId': '2'},
                    ]
                },
                '_links': {
                    'next': {'href': 'next_page'}
                }
            }
        }
    }
    page2 = {
        '_embedded': {
            'episodes': {
                '_embedded': {
                    'episodes': [
                        {'prfId': '3'}
                    ]
                },
                '_links': {
                    'next': {'href': 'no_more'}
                }
            }
        }
    }
    # Mock _call_api to return page2 on first call, then None
    call_order = []

    def mock_call_api(path, video_id, item=None, note=None, fatal=True, query=None):
        call_order.append(path)
        if path == 'next_page':
            return page2
        return None

    monkeypatch.setattr(ie, '_call_api', mock_call_api)

    # Collect entries
    entries = list(ie._entries(page1, 'display'))
    # Should have 3 entries
    assert len(entries) == 3
    assert [e.url for e in entries] == ['nrk:1', 'nrk:2', 'nrk:3']
    # Ensure _call_api was called with correct next path
    assert call_order == ['next_page']
