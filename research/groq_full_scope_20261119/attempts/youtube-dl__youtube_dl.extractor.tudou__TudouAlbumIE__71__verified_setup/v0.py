import pytest
from youtube_dl.extractor.tudou import TudouAlbumIE


class DummyDownloader:
    """A minimal downloader that only implements _download_json."""
    def __init__(self, json_data):
        self.json_data = json_data

    def _download_json(self, url, video_id, note=None, errnote=None, headers=None, data=None, timeout=None, add_dto=None):
        # Return the pre‑provided JSON data regardless of URL
        return self.json_data


def test_normal_extraction(tmp_path):
    # Prepare dummy JSON data with 3 items
    dummy_json = {
        'items': [
            {'icode': 'abc123', 'kw': 'video1'},
            {'icode': 'def456', 'kw': 'video2'},
            {'icode': 'ghi789', 'kw': 'video3'},
        ]
    }
    downloader = DummyDownloader(dummy_json)
    ie = TudouAlbumIE(downloader=downloader)

    # Use a valid URL that matches the regex
    url = 'http://www.tudou.com/albumplay/xyzABC12345.html'
    result = ie.extract(url)

    # The result should be a playlist with 3 entries
    assert result['entries'] is not None
    assert len(result['entries']) == 3
    # Each entry should be a dict with expected keys
    for entry, item in zip(result['entries'], dummy_json['items']):
        assert entry['url'] == f'http://www.tudou.com/programs/view/{item["icode"]}'
        assert entry['ie_key'] == 'Tudou'
        assert entry['id'] == item['icode']
        assert entry['title'] == item['kw']


def test_empty_items(tmp_path):
    # Dummy JSON with no items
    dummy_json = {'items': []}
    downloader = DummyDownloader(dummy_json)
    ie = TudouAlbumIE(downloader=downloader)

    url = 'http://www.tudou.com/albumcover/12345678901.html'
    result = ie.extract(url)

    # Playlist should contain zero entries
    assert result['entries'] == []
    assert result['id'] == '12345678901'


def test_invalid_url_raises():
    # Use a URL that does not match the regex
    ie = TudouAlbumIE()
    with pytest.raises(ValueError):
        ie.extract('http://www.example.com/not-a-tudou-url')
