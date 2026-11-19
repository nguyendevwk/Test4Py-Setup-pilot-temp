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


def test_single_item_playlist(tmp_path):
    """Test extraction when the playlist contains a single item."""
    dummy_items = [{'icode': 'single123', 'kw': 'singlekw'}]
    dummy_json = {'items': dummy_items}
    downloader = DummyDownloader(dummy_json)

    ie = TudouPlaylistIE()
    ie.downloader = downloader

    result = ie.extract('http://www.tudou.com/listplay/abcd1234xyz.html')
    assert result['entries'] == [
        {
            'url': 'http://www.tudou.com/programs/view/single123',
            'ie_key': 'Tudou',
            'id': 'single123',
            'title': 'singlekw',
        }
    ]


def test_invalid_url_raises_error(tmp_path):
    """Ensure that an invalid URL raises a ValueError."""
    ie = TudouPlaylistIE()
    with pytest.raises(ValueError):
        ie.extract('http://www.invalid.com/not_a_tudou_playlist.html')
