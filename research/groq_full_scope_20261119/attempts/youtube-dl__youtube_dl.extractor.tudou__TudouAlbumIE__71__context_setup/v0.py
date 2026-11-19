import pytest
from youtube_dl.extractor.tudou import TudouAlbumIE


class DummyDownloader:
    """A minimal downloader that records the last URL requested."""
    def __init__(self, json_data):
        self.json_data = json_data
        self.last_url = None

    def urlopen(self, url):
        self.last_url = url
        return None  # Not used

    def _download_json(self, url, video_id, note=None, errnote=None, headers=None, data=None, timeout=None):
        self.last_url = url
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

    result = ie.extract('http://www.tudou.com/albumplay/xyzABC12345.html')
    assert result['id'] == 'xyzABC12345'
    assert result['entries'] == [
        {
            'url': 'http://www.tudou.com/programs/view/abc123',
            'ie_key': 'Tudou',
            'id': 'abc123',
            'title': 'video1',
        },
        {
            'url': 'http://www.tudou.com/programs/view/def456',
            'ie_key': 'Tudou',
            'id': 'def456',
            'title': 'video2',
        },
        {
            'url': 'http://www.tudou.com/programs/view/ghi789',
            'ie_key': 'Tudou',
            'id': 'ghi789',
            'title': 'video3',
        },
    ]
    # Ensure the downloader was called with the correct API URL
    assert downloader.last_url == 'http://www.tudou.com/tvp/alist.action?acode=xyzABC12345'


def test_empty_playlist(tmp_path):
    # Dummy JSON with no items
    dummy_json = {'items': []}
    downloader = DummyDownloader(dummy_json)
    ie = TudouAlbumIE(downloader=downloader)

    result = ie.extract('http://www.tudou.com/albumcover/12345678901.html')
    assert result['id'] == '12345678901'
    assert result['entries'] == []  # Empty playlist
    assert downloader.last_url == 'http://www.tudou.com/tvp/alist.action?acode=12345678901'


def test_invalid_url_raises():
    ie = TudouAlbumIE()
    with pytest.raises(ValueError):
        ie.extract('https://example.com/not-a-tudou-url')
