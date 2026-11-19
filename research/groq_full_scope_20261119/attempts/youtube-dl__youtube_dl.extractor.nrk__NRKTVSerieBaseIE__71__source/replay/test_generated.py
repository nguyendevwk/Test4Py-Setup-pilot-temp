import pytest
from youtube_dl.extractor.nrk import NRKTVSerieBaseIE

# Helper dummy class to avoid needing the full NRKBaseIE implementation
class DummyIE(NRKTVSerieBaseIE):
    def __init__(self, api_responses=None):
        super().__init__()
        self.api_responses = api_responses or {}
        self.calls = []

    def _call_api(self, url, display_id, note=None, fatal=False):
        self.calls.append((url, display_id))
        return self.api_responses.get(url)

    def url_result(self, url, ie=None, video_id=None):
        # Return a simple tuple that can be asserted against
        return (url, ie, video_id)

# Monkeypatch NRKIE.ie_key to avoid missing dependency
NRKTVSerieBaseIE.__module__ = 'youtube_dl.extractor.nrk'
try:
    from youtube_dl.extractor.nrk import NRKIE
    NRKIE.ie_key = staticmethod(lambda: 'mockIE')
except Exception:
    # If NRKIE is not importable, define a minimal stub
    class NRKIE:
        @staticmethod
        def ie_key():
            return 'mockIE'


def test_entries_single_page():
    """Test that _entries yields correct entries for a single page with episodes."""
    data = {
        '_embedded': {
            'episodes': {
                '_embedded': {
                    'episodes': [
                        {'prfId': '123'},
                        {'episodeId': '456'},
                        {'prfId': None},          # should be skipped
                        {'prfId': 789},           # not a string, should be skipped
                    ]
                }
            }
        }
    }
    dummy = DummyIE()
    entries = list(dummy._entries(data, display_id='test'))
    assert len(entries) == 2
    assert entries[0] == ('nrk:123', 'mockIE', '123')
    assert entries[1] == ('nrk:456', 'mockIE', '456')


def test_extract_entries_non_list():
    """Test that _extract_entries returns an empty list when input is not a list."""
    dummy = DummyIE()
    assert dummy._extract_entries({'prfId': '123'}) == []


def test_entries_next_page_and_stop_on_none():
    """Test that _entries follows next links and stops when API returns None."""
    # First page data
    first_page = {
        '_embedded': {
            'instalments': {
                '_embedded': {
                    'instalments': [
                        {'prfId': 'a'},
                        {'episodeId': 'b'}
                    ]
                },
                '_links': {
                    'next': {'href': 'next_page'}
                }
            }
        }
    }
    # Second page data returned by _call_api
    second_page = {
        '_embedded': {
            'instalments': {
                '_embedded': {
                    'instalments': [
                        {'prfId': 'c'}
                    ]
                }
            }
        }
    }
    dummy = DummyIE(api_responses={'next_page': second_page})
    entries = list(dummy._entries(first_page, display_id='test'))
    # Should have 3 entries from both pages
    assert len(entries) == 3
    urls = [e[0] for e in entries]
    assert 'nrk:a' in urls
    assert 'nrk:b' in urls
    assert 'nrk:c' in urls
    # Ensure _call_api was called with the correct URL
    assert dummy.calls == [('next_page', 'test')]
