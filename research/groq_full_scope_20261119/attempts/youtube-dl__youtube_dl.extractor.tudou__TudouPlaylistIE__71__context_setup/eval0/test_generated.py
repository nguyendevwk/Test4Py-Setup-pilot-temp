import json
import pytest
from youtube_dl.extractor.tudou import TudouPlaylistIE


class DummyDownloader:
    """A minimal downloader that returns predefined JSON data."""
    def __init__(self, data):
        self.data = data

    def _download_json(self, url, video_id, note=None, errnote=None, headers=None, data=None, timeout=None, check_status=True):
        # Return the predefined data regardless of the URL
        return self.data


def test_playlist_minimum_entries(tmp_path):
    """Verify that the playlist contains at least the expected number of entries."""
    # Prepare dummy playlist data with 209 items
    dummy_items = [{'icode': f'id{i}', 'kw': f'kw{i}'} for i in range(209)]
    dummy_json = {'items': dummy_items}
    downloader = DummyDownloader(dummy_json)

    ie = TudouPlaylistIE()
    ie.downloader = downloader

    result = ie.extract('http://www.tudou.com/listplay/zzdE77v6Mmo.html')
    assert result['entries'] is not None
    assert len(result['entries']) == 209
    assert all(entry['url'] == f'http://www.tudou.com/programs/view/{item["icode"]}' for entry, item in zip(result['entries'], dummy_items))


def test_invalid_url_raises():
    """Ensure that an invalid URL raises a ValueError."""
    ie = TudouPlaylistIE()
    with pytest.raises(ValueError):
        ie.extract('http://www.tudou.com/invalid/zzdE77v6Mmo.html')


def test_entry_fields_correct(tmp_path):
    """Check that each entry contains the expected keys and values."""
    dummy_items = [
        {'icode': 'abc123', 'kw': 'keyword1'},
        {'icode': 'def456', 'kw': 'keyword2'},
    ]
    dummy_json = {'items': dummy_items}
    downloader = DummyDownloader(dummy_json)

    ie = TudouPlaylistIE()
    ie.downloader = downloader

    result = ie.extract('http://www.tudou.com/listplay/zzdE77v6Mmo.html')
    entries = result['entries']
    assert len(entries) == 2
    for entry, item in zip(entries, dummy_items):
        assert entry['url'] == f'http://www.tudou.com/programs/view/{item["icode"]}'
        assert entry['ie_key'] == 'Tudou'
        assert entry['id'] == item['icode']
        assert entry['title'] == item['kw']
