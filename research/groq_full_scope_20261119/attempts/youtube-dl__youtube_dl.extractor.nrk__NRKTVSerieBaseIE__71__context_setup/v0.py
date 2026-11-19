import pytest
from youtube_dl.extractor.nrk import NRKTVSerieBaseIE, NRKIE


class DummyIE(NRKTVSerieBaseIE):
    """A minimal stub of NRKTVSerieBaseIE for testing."""

    def url_result(self, url, ie=None, video_id=None):
        # Return a tuple that mimics the real url_result output
        return (url, ie, video_id)

    def _call_api(self, *args, **kwargs):
        # Return None to stop pagination in _entries
        return None


def test_extract_entries_filters_and_formats():
    dummy = DummyIE()
    # Valid entries: correct type and string id
    entry_list = [
        {"prfId": "12345"},
        {"episodeId": "abcde"},
        {"prfId": 67890},          # invalid type
        {"episodeId": None},       # missing id
        {"otherKey": "value"}      # no id key
    ]
    result = dummy._extract_entries(entry_list)
    # Should contain two entries with correct URLs and video_ids
    assert len(result) == 2
    assert result[0] == ("nrk:12345", NRKIE.ie_key(), "12345")
    assert result[1] == ("nrk:abcde", NRKIE.ie_key(), "abcde")


def test_extract_assets_key_returns_first_match():
    dummy = DummyIE()
    # _ASSETS_KEYS = ('episodes', 'instalments',)
    data = {"instalments": [], "episodes": []}
    # Should return 'episodes' because it appears first in the tuple
    assert dummy._extract_assets_key(data) == "episodes"

    data = {"instalments": []}
    assert dummy._extract_assets_key(data) == "instalments"

    data = {"other": []}
    assert dummy._extract_assets_key(data) is None


def test_entries_yields_all_episodes_and_stops_on_no_next():
    dummy = DummyIE()
    # Prepare a data structure that mimics the API response
    data = {
        "_embedded": {
            "episodes": {
                "_embedded": {
                    "episodes": [
                        {"prfId": "e1"},
                        {"prfId": "e2"},
                    ]
                },
                "_links": {
                    "next": {"href": "next_page"}
                }
            }
        }
    }
    # Override _call_api to return None so pagination stops after first page
    dummy._call_api = lambda *_, **__: None

    entries = list(dummy._entries(data, display_id="test"))
    # Should yield two entries corresponding to the two episodes
    assert len(entries) == 2
    assert entries[0] == ("nrk:e1", NRKIE.ie_key(), "e1")
    assert entries[1] == ("nrk:e2", NRKIE.ie_key(), "e2")
